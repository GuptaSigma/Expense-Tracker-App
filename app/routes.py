from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify
from flask_login import login_required, current_user
from app import db
from app.models import Expense, Income, Watchlist
from app.ml_model import SpendingPredictor, BudgetOptimizer
from app.market_data import get_market_data, get_investment_advice, search_stocks, get_stock_price, get_all_sectors
from app.local_chatbot import LocalAIChatbot
from app.gemini_chatbot import GeminiChatbot
from app.openrouter_advisor import OpenRouterAdvisor
from app.utils import BUDGET_PERCENTAGES
from flask import current_app
from datetime import datetime, timedelta
import json
import logging

logger = logging.getLogger(__name__)

main = Blueprint('main', __name__)
predictor = SpendingPredictor()
optimizer = BudgetOptimizer()

# Initialize Gemini Chatbot for chatbox (with OpenRouter + local fallback)
def get_chatbot():
    """Get or create Gemini chatbot instance with fallbacks"""
    if not hasattr(get_chatbot, 'instance'):
        gemini_key = current_app.config.get('GEMINI_API_KEY')
        gemini_model = current_app.config.get('GEMINI_MODEL', 'gemini-2.0-flash')
        openrouter_key = current_app.config.get('OPENROUTER_API_KEY')
        openrouter_model = current_app.config.get('OPENROUTER_MODEL', 'openai/gpt-4o-mini')
        
        # Try Gemini first, with OpenRouter as fallback
        get_chatbot.instance = GeminiChatbot(
            gemini_key=gemini_key,
            openrouter_key=openrouter_key,
            gemini_model=gemini_model,
            openrouter_model=openrouter_model
        )
    return get_chatbot.instance

# Initialize OpenRouter Advisor for investment suggestions
def get_openrouter_advisor():
    """Get or create OpenRouter advisor instance"""
    if not hasattr(get_openrouter_advisor, 'instance'):
        api_key = current_app.config.get('OPENROUTER_API_KEY')
        model = current_app.config.get('OPENROUTER_MODEL', 'openai/gpt-4o-mini')
        if api_key:
            get_openrouter_advisor.instance = OpenRouterAdvisor(api_key, model)
        else:
            get_openrouter_advisor.instance = None
    return get_openrouter_advisor.instance

@main.route('/')
def index():
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))
    return render_template('home.html')

@main.route('/dashboard')
@login_required
def dashboard():
    # Get user's recent expenses
    recent_expenses_query = Expense.query.filter_by(user_id=current_user.id)\
        .order_by(Expense.date.desc()).limit(10).all()
    
    # Serialize expenses for JSON
    recent_expenses = recent_expenses_query
    recent_expenses_json = [{
        'date': expense.date.strftime('%Y-%m-%d'),
        'category': expense.category,
        'description': expense.description or '',
        'amount': float(expense.amount)
    } for expense in recent_expenses_query]
    
    # Calculate totals
    total_expense = db.session.query(db.func.sum(Expense.amount))\
        .filter_by(user_id=current_user.id).scalar() or 0
    
    total_income = db.session.query(db.func.sum(Income.amount))\
        .filter_by(user_id=current_user.id).scalar() or 0
    
    # Category breakdown
    categories = db.session.query(Expense.category, db.func.sum(Expense.amount))\
        .filter_by(user_id=current_user.id)\
        .group_by(Expense.category).all()
    
    # Prepare data for charts
    category_labels = [c[0] for c in categories]
    category_data = [float(c[1]) for c in categories]
    
    # Budget tracking - percentage-based allocation for current month

    # Monthly income (current month only) — budget missing means no alerts
    first_of_month = datetime.now().replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    monthly_income = db.session.query(db.func.sum(Income.amount))\
        .filter(
            Income.user_id == current_user.id,
            Income.date >= first_of_month
        ).scalar() or 0

    dynamic_budgets = {}
    if monthly_income > 0:
        for category, percentage in BUDGET_PERCENTAGES.items():
            dynamic_budgets[category] = round(monthly_income * (percentage / 100), 2)
        min_spend_threshold = max(500, monthly_income * 0.05)
    else:
        for category in BUDGET_PERCENTAGES:
            dynamic_budgets[category] = 0
        min_spend_threshold = 0

    # Calculate budget progress using current month's expenses
    budget_progress = []
    for category, budget_limit in dynamic_budgets.items():
        monthly_spent = db.session.query(db.func.sum(Expense.amount))\
            .filter(
                Expense.user_id == current_user.id,
                Expense.category == category,
                Expense.date >= first_of_month
            ).scalar() or 0
        percentage = (monthly_spent / budget_limit * 100) if budget_limit > 0 else 0

        # Determine status using new rule
        if budget_limit == 0:
            status = 'safe'
            color = 'green'
        elif monthly_spent >= budget_limit and monthly_spent >= min_spend_threshold:
            status = 'danger'
            color = 'red'
        elif monthly_spent >= 0.8 * budget_limit and monthly_spent >= min_spend_threshold:
            status = 'caution'
            color = 'yellow'
        else:
            status = 'safe'
            color = 'green'

        budget_progress.append({
            'category': category,
            'spent': float(monthly_spent),
            'limit': budget_limit,
            'percentage': min(percentage, 100),
            'status': status,
            'color': color,
            'remaining': max(budget_limit - monthly_spent, 0)
        })
    
    # AI Predictions
    predictions = predictor.predict_next_month(current_user.id)
    insights = optimizer.generate_insights(current_user.id)
    ai_suggestions = optimizer.get_ai_suggestions(current_user.id)
    
    # Advanced Charts Data
    # 1. Daily expense trend (last 30 days)
    thirty_days_ago = datetime.now() - timedelta(days=30)
    
    daily_expenses_query = db.session.query(
        db.func.date(Expense.date).label('day'),
        db.func.sum(Expense.amount).label('total')
    ).filter(
        Expense.user_id == current_user.id,
        Expense.date >= thirty_days_ago
    ).group_by(db.func.date(Expense.date)).all()
    
    # Fill in missing days with 0
    expense_trend_labels = []
    expense_trend_data = []
    daily_expenses_dict = {str(d.day): float(d.total) for d in daily_expenses_query}
    
    for i in range(30):
        day = (datetime.now() - timedelta(days=29-i)).strftime('%Y-%m-%d')
        expense_trend_labels.append((datetime.now() - timedelta(days=29-i)).strftime('%b %d'))
        expense_trend_data.append(daily_expenses_dict.get(day, 0))
    
    # 2. Monthly comparison (last 6 months) - correct calendar month arithmetic
    monthly_data = []
    now = datetime.now()
    for i in range(6):
        # Subtract i months using safe calendar arithmetic (no timedelta approximation)
        years_back = i // 12
        months_back = i % 12
        month = now.month - months_back
        if month <= 0:
            month += 12
            years_back += 1
        year = now.year - years_back

        month_start = datetime(year, month, 1)
        if month == 12:
            next_month_start = datetime(year + 1, 1, 1)
        else:
            next_month_start = datetime(year, month + 1, 1)

        month_expense = db.session.query(db.func.sum(Expense.amount))\
            .filter(
                Expense.user_id == current_user.id,
                Expense.date >= month_start,
                Expense.date < next_month_start
            ).scalar() or 0

        month_income = db.session.query(db.func.sum(Income.amount))\
            .filter(
                Income.user_id == current_user.id,
                Income.date >= month_start,
                Income.date < next_month_start
            ).scalar() or 0

        monthly_data.append({
            'month': month_start.strftime('%b %Y'),
            'income': float(month_income),
            'expense': float(month_expense)
        })
    
    monthly_data.reverse()
    monthly_labels = [m['month'] for m in monthly_data]
    monthly_income_data = [m['income'] for m in monthly_data]
    monthly_expense_data = [m['expense'] for m in monthly_data]
    
    # Get user's watchlist (latest 10)
    user_watchlist = Watchlist.query.filter_by(user_id=current_user.id)\
        .order_by(Watchlist.added_date.desc()).limit(10).all()
    
    return render_template('dashboard.html',
                         recent_expenses=recent_expenses,
                         recent_expenses_json=recent_expenses_json,
                         total_expense=total_expense,
                         total_income=total_income,
                         balance=total_income - total_expense,
                         category_labels=category_labels,
                         category_data=category_data,
                         budget_progress=budget_progress,
                         expense_trend_labels=expense_trend_labels,
                         expense_trend_data=expense_trend_data,
                         monthly_labels=monthly_labels,
                         monthly_income_data=monthly_income_data,
                         monthly_expense_data=monthly_expense_data,
                         predictions=predictions,
                         insights=insights,
                         ai_suggestions=ai_suggestions,
                         user_watchlist=user_watchlist)

@main.route('/add_expense', methods=['GET', 'POST'])
@login_required
def add_expense():
    if request.method == 'POST':
        expense = Expense(
            amount=float(request.form.get('amount')),
            category=request.form.get('category'),
            description=request.form.get('description'),
            user_id=current_user.id
        )
        db.session.add(expense)
        db.session.commit()
        
        # Check for overspending alert
        alert_level = optimizer.check_overspending(current_user.id, expense.category)
        if alert_level == 'alert':
            flash(f'Alert: You have exceeded your {expense.category} budget this month!', 'error')
        elif alert_level == 'warning':
            flash(f'Warning: You are nearing your {expense.category} budget limit this month!', 'warning')
        else:
            flash('Expense added successfully!', 'success')
        
        return redirect(url_for('main.dashboard'))
    
    return render_template('add_expense.html')

@main.route('/add_income', methods=['GET', 'POST'])
@login_required
def add_income():
    if request.method == 'POST':
        income = Income(
            amount=float(request.form.get('amount')),
            source=request.form.get('source'),
            description=request.form.get('description', ''),
            user_id=current_user.id
        )
        db.session.add(income)
        db.session.commit()
        flash('Income added successfully!', 'success')
        return redirect(url_for('main.dashboard'))
    
    return render_template('add_income.html')

# ============= DELETE ROUTES =============
@main.route('/delete_expense/<int:expense_id>', methods=['POST'])
@login_required
def delete_expense(expense_id):
    """Delete an expense entry"""
    expense = Expense.query.filter_by(id=expense_id, user_id=current_user.id).first()
    if not expense:
        flash('Expense not found!', 'error')
    else:
        db.session.delete(expense)
        db.session.commit()
        flash(f'Expense of ₹{expense.amount} deleted successfully!', 'success')
    return redirect(url_for('main.dashboard'))

@main.route('/delete_income/<int:income_id>', methods=['POST'])
@login_required
def delete_income(income_id):
    """Delete an income entry"""
    income = Income.query.filter_by(id=income_id, user_id=current_user.id).first()
    if not income:
        flash('Income not found!', 'error')
    else:
        db.session.delete(income)
        db.session.commit()
        flash(f'Income of ₹{income.amount} deleted successfully!', 'success')
    return redirect(url_for('main.dashboard'))

# ============= EDIT ROUTES =============
@main.route('/edit_expense/<int:expense_id>', methods=['GET', 'POST'])
@login_required
def edit_expense(expense_id):
    """Edit existing expense"""
    expense = Expense.query.filter_by(id=expense_id, user_id=current_user.id).first()
    if not expense:
        flash('Expense not found!', 'error')
        return redirect(url_for('main.dashboard'))
    
    if request.method == 'POST':
        expense.amount = float(request.form.get('amount'))
        expense.category = request.form.get('category')
        expense.description = request.form.get('description')
        db.session.commit()
        flash('Expense updated successfully!', 'success')
        return redirect(url_for('main.dashboard'))
    
    return render_template('edit_expense.html', expense=expense)

@main.route('/edit_income/<int:income_id>', methods=['GET', 'POST'])
@login_required
def edit_income(income_id):
    """Edit existing income"""
    income = Income.query.filter_by(id=income_id, user_id=current_user.id).first()
    if not income:
        flash('Income not found!', 'error')
        return redirect(url_for('main.dashboard'))
    
    if request.method == 'POST':
        income.amount = float(request.form.get('amount'))
        income.source = request.form.get('source')
        income.description = request.form.get('description', '')
        db.session.commit()
        flash('Income updated successfully!', 'success')
        return redirect(url_for('main.dashboard'))
    
    return render_template('edit_income.html', income=income)

@main.route('/api/expense_data')
@login_required
def expense_data():
    # For AJAX calls to update charts
    last_7_days = datetime.now() - timedelta(days=7)
    daily_expenses = db.session.query(
        db.func.date(Expense.date), 
        db.func.sum(Expense.amount)
    ).filter(
        Expense.user_id == current_user.id,
        Expense.date >= last_7_days
    ).group_by(db.func.date(Expense.date)).all()
    
    return jsonify({
        'dates': [str(d[0]) for d in daily_expenses],
        'amounts': [float(d[1]) for d in daily_expenses]
    })

@main.route('/market')
@login_required
def market_watch():
    """Real-time market data and investment opportunities"""
    market_data = get_market_data()
    
    # Get user's balance and spending
    total_income = db.session.query(db.func.sum(Income.amount))\
        .filter_by(user_id=current_user.id).scalar() or 0
    total_expense = db.session.query(db.func.sum(Expense.amount))\
        .filter_by(user_id=current_user.id).scalar() or 0
    user_balance = total_income - total_expense
    
    # Get investment recommendations
    spending_data = db.session.query(
        Expense.category,
        db.func.sum(Expense.amount).label('total')
    ).filter_by(user_id=current_user.id).group_by(Expense.category).all()
    
    spending_dict = {'monthly_expenses': [c[1] for c in spending_data]}
    recommendations = get_investment_advice(user_balance, spending_dict)
    
    # Get investment coaching
    investment_coach = optimizer.get_investment_coach(
        current_user.id,
        user_balance,
        total_income,
        total_expense
    )
    
    return render_template('market_watch.html',
                         market_data=market_data,
                         recommendations=recommendations,
                         investment_coach=investment_coach,
                         user_balance=user_balance)

@main.route('/api/market_data')
@login_required
def api_market_data():
    """API endpoint for real-time market updates"""
    try:
        market_data = get_market_data()
        return jsonify({
            'status': 'success',
            'data': market_data
        })
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

@main.route('/investment-coach')
@login_required
def investment_coach():
    """AI-powered investment coaching page"""
    total_income = db.session.query(db.func.sum(Income.amount))\
        .filter_by(user_id=current_user.id).scalar() or 0
    total_expense = db.session.query(db.func.sum(Expense.amount))\
        .filter_by(user_id=current_user.id).scalar() or 0
    user_balance = total_income - total_expense
    
    # Get investment coaching
    coaching = optimizer.get_investment_coach(
        current_user.id,
        user_balance,
        total_income,
        total_expense
    )
    
    # Get market data for context
    market_data = get_market_data()
    
    return render_template('investment_coach.html',
                         coaching=coaching,
                         market_data=market_data,
                         user_balance=user_balance,
                         monthly_income=total_income,
                         monthly_expense=total_expense)


@main.route('/stock-search')
@login_required
def stock_search():
    """Stock search page"""
    query = request.args.get('q', '').strip()
    sector_filter = request.args.get('sector', '')
    
    results = []
    sectors = get_all_sectors()
    
    if query:
        results = search_stocks(query)
    elif sector_filter:
        # Filter by sector
        from app.market_data import ALL_STOCKS
        results = [s for s in ALL_STOCKS if s['sector'].lower() == sector_filter.lower()]
        for r in results:
            change_24h = __import__('random').uniform(-3, 3)
            r['current_price'] = r['base_price'] * (1 + change_24h/100)
            r['change_24h'] = round(change_24h, 2)
    
    # Get user's watchlist
    user_watchlist = Watchlist.query.filter_by(user_id=current_user.id).all()
    watchlist_symbols = [w.symbol for w in user_watchlist]
    
    return render_template('stock_search.html',
                         results=results,
                         sectors=sectors,
                         query=query,
                         sector_filter=sector_filter,
                         watchlist_symbols=watchlist_symbols)


@main.route('/api/stock-search')
@login_required
def api_stock_search():
    """API endpoint for stock search with JSON response"""
    query = request.args.get('q', '').strip()
    if not query or len(query) < 1:
        return jsonify([])
    
    results = search_stocks(query, limit=15)
    return jsonify(results)


@main.route('/watchlist/add/<symbol>', methods=['POST'])
@login_required
def add_to_watchlist(symbol):
    """Add stock to user's watchlist"""
    symbol = symbol.upper()
    stock = get_stock_price(symbol)
    
    if not stock:
        flash('Stock not found!', 'danger')
        return redirect(request.referrer or url_for('main.stock_search'))
    
    # Check if already in watchlist
    existing = Watchlist.query.filter_by(
        user_id=current_user.id,
        symbol=symbol
    ).first()
    
    if existing:
        flash(f'{symbol} is already in your watchlist!', 'info')
    else:
        watchlist_item = Watchlist(
            user_id=current_user.id,
            symbol=symbol,
            name=stock['name'],
            sector=stock['sector']
        )
        db.session.add(watchlist_item)
        db.session.commit()
        flash(f'{symbol} added to your watchlist!', 'success')
    
    return redirect(request.referrer or url_for('main.stock_search'))


@main.route('/watchlist/remove/<symbol>', methods=['POST'])
@login_required
def remove_from_watchlist(symbol):
    """Remove stock from user's watchlist"""
    watchlist_item = Watchlist.query.filter_by(
        user_id=current_user.id,
        symbol=symbol.upper()
    ).first()
    
    if watchlist_item:
        db.session.delete(watchlist_item)
        db.session.commit()
        flash(f'{symbol} removed from your watchlist!', 'success')
    else:
        flash('Stock not found in watchlist!', 'danger')
    
    return redirect(request.referrer or url_for('main.watchlist'))


@main.route('/watchlist')
@login_required
def watchlist():
    """View user's stock watchlist with current prices"""
    user_watchlist = Watchlist.query.filter_by(user_id=current_user.id)\
        .order_by(Watchlist.added_date.desc()).all()
    
    # Get current prices for all watched stocks
    watchlist_data = []
    for item in user_watchlist:
        stock = get_stock_price(item.symbol)
        if stock:
            watchlist_data.append(stock)
    
    return render_template('watchlist.html', watchlist=watchlist_data)


@main.route('/api/watchlist')
@login_required
def api_watchlist():
    """API endpoint for watchlist data"""
    user_watchlist = Watchlist.query.filter_by(user_id=current_user.id).all()
    
    watchlist_data = []
    for item in user_watchlist:
        stock = get_stock_price(item.symbol)
        if stock:
            watchlist_data.append(stock)
    
    return jsonify(watchlist_data)


@main.route('/api/chat', methods=['POST'])
@login_required
def api_chat():
    """AI Fin-Buddy Chat API Endpoint - Uses Gemini API"""
    try:
        data = request.get_json()
        user_message = data.get('message', '').strip()
        
        if not user_message:
            return jsonify({'status': 'error', 'message': 'Empty message'}), 400
        
        # Prepare user context
        total_income = db.session.query(db.func.sum(Income.amount))\
            .filter_by(user_id=current_user.id).scalar() or 0
        total_expense = db.session.query(db.func.sum(Expense.amount))\
            .filter_by(user_id=current_user.id).scalar() or 0
        user_balance = total_income - total_expense
        
        # Get spending by category
        spending_data = db.session.query(
            Expense.category,
            db.func.sum(Expense.amount).label('total')
        ).filter_by(user_id=current_user.id).group_by(Expense.category).all()
        
        expenses = {c[0]: c[1] for c in spending_data}
        
        # Get market data
        market_data = get_market_data()
        
        # Prepare context for chatbot
        user_context = {
            'username': current_user.username,
            'balance': user_balance,
            'market_data': {
                'gold_price': market_data['gold']['gold_price_24k'],
                'bitcoin_price': market_data['crypto']['bitcoin']['price'],
                'ethereum_price': market_data['crypto']['ethereum']['price'],
                'nifty_50': market_data['indices']['nifty_50']['price'],
                'sp500': market_data['indices']['sp500']['price'],
            },
            'expenses': expenses,
        }
        
        # Get chatbot (Gemini with local fallback)
        chatbot = get_chatbot()
        ai_response = chatbot.chat(user_message, user_context)
        
        return jsonify({
            'status': 'success',
            'message': ai_response,
            'timestamp': datetime.now().isoformat()
        })
        
    except Exception as e:
        logger.error(f"Chat API error: {str(e)}")
        return jsonify({
            'status': 'error',
            'message': 'Oops! Kuch error aaya. Dobara try karein! 🤖'
        }), 500

@main.route('/api/investment-advice', methods=['GET'])
@login_required
def api_investment_advice():
    """Get investment advice from OpenRouter API"""
    try:
        # Prepare user context
        total_income = db.session.query(db.func.sum(Income.amount))\
            .filter_by(user_id=current_user.id).scalar() or 0
        total_expense = db.session.query(db.func.sum(Expense.amount))\
            .filter_by(user_id=current_user.id).scalar() or 0
        user_balance = total_income - total_expense
        
        # Get spending by category
        spending_data = db.session.query(
            Expense.category,
            db.func.sum(Expense.amount).label('total')
        ).filter_by(user_id=current_user.id).group_by(Expense.category).all()
        
        expenses = {c[0]: c[1] for c in spending_data}
        
        # Get market data
        market_data = get_market_data()
        
        # Prepare context
        user_context = {
            'username': current_user.username,
            'balance': user_balance,
            'market_data': {
                'gold_price': market_data['gold']['gold_price_24k'],
                'bitcoin_price': market_data['crypto']['bitcoin']['price'],
                'ethereum_price': market_data['crypto']['ethereum']['price'],
                'nifty_50': market_data['indices']['nifty_50']['price'],
                'sp500': market_data['indices']['sp500']['price'],
            },
            'expenses': expenses,
        }
        
        # Get OpenRouter advisor
        advisor = get_openrouter_advisor()
        
        if advisor:
            advice = advisor.get_investment_advice(user_context)
        else:
            # Fallback if no OpenRouter key
            from app.local_chatbot import LocalAIChatbot
            local_bot = LocalAIChatbot()
            advice = local_bot.chat("Mujhe investment advice de", user_context)
        
        return jsonify({
            'status': 'success',
            'advice': advice,
            'timestamp': datetime.now().isoformat()
        })
        
    except Exception as e:
        logger.error(f"Investment advice error: {str(e)}")
        return jsonify({
            'status': 'error',
            'message': 'Investment advice fetch failed. Try again!'
        }), 500

@main.route('/calculators')
@login_required
def calculators():
    """Financial Calculators Page"""
    return render_template('calculators.html')

@main.route('/achievements')
@login_required
def achievements():
    """User Achievements and Gamification Page"""
    # Calculate user stats
    total_income = db.session.query(db.func.sum(Income.amount))\
        .filter_by(user_id=current_user.id).scalar() or 0
    total_expense = db.session.query(db.func.sum(Expense.amount))\
        .filter_by(user_id=current_user.id).scalar() or 0
    user_balance = total_income - total_expense
    
    # Count transactions
    income_count = Income.query.filter_by(user_id=current_user.id).count()
    expense_count = Expense.query.filter_by(user_id=current_user.id).count()
    watchlist_count = Watchlist.query.filter_by(user_id=current_user.id).count()
    
    # Calculate savings rate
    savings_rate = 0
    if total_income > 0:
        savings_rate = ((total_income - total_expense) / total_income) * 100
    
    # Calculate streak (simplified - days with transactions)
    from datetime import datetime, timedelta
    today = datetime.now().date()
    streak = 0
    current_date = today
    
    # Check for continuous days with transactions
    for i in range(30):  # Check last 30 days
        has_transaction = (
            Expense.query.filter(
                Expense.user_id == current_user.id,
                db.func.date(Expense.date) == current_date
            ).first() is not None or
            Income.query.filter(
                Income.user_id == current_user.id,
                db.func.date(Income.date) == current_date
            ).first() is not None
        )
        
        if has_transaction:
            streak += 1
            current_date = current_date - timedelta(days=1)
        else:
            break
    
    # Calculate level based on total transactions
    total_transactions = income_count + expense_count
    level = 1 + (total_transactions // 10)  # Level up every 10 transactions
    next_level_transactions = (level * 10)
    level_progress = ((total_transactions % 10) / 10) * 100
    
    # Define achievements
    achievements_list = [
        {
            'id': 'first_income',
            'name': 'First Steps',
            'description': 'Log your first income',
            'icon': 'bi-currency-rupee',
            'color': 'from-green-500 to-emerald-600',
            'unlocked': income_count >= 1,
            'progress': min(100, (income_count / 1) * 100)
        },
        {
            'id': 'first_expense',
            'name': 'Spender',
            'description': 'Track your first expense',
            'icon': 'bi-cash-coin',
            'color': 'from-red-500 to-pink-600',
            'unlocked': expense_count >= 1,
            'progress': min(100, (expense_count / 1) * 100)
        },
        {
            'id': 'ten_transactions',
            'name': 'Getting Started',
            'description': 'Complete 10 transactions',
            'icon': 'bi-graph-up',
            'color': 'from-blue-500 to-indigo-600',
            'unlocked': total_transactions >= 10,
            'progress': min(100, (total_transactions / 10) * 100)
        },
        {
            'id': 'fifty_transactions',
            'name': 'Dedicated Tracker',
            'description': 'Complete 50 transactions',
            'icon': 'bi-trophy',
            'color': 'from-purple-500 to-pink-600',
            'unlocked': total_transactions >= 50,
            'progress': min(100, (total_transactions / 50) * 100)
        },
        {
            'id': 'positive_balance',
            'name': 'Profit Maker',
            'description': 'Maintain positive balance',
            'icon': 'bi-piggy-bank',
            'color': 'from-green-500 to-teal-600',
            'unlocked': user_balance > 0,
            'progress': 100 if user_balance > 0 else 0
        },
        {
            'id': 'high_saver',
            'name': 'High Saver',
            'description': 'Achieve 50%+ savings rate',
            'icon': 'bi-gem',
            'color': 'from-amber-500 to-orange-600',
            'unlocked': savings_rate >= 50,
            'progress': min(100, (savings_rate / 50) * 100)
        },
        {
            'id': 'market_watcher',
            'name': 'Market Watcher',
            'description': 'Add 5 stocks to watchlist',
            'icon': 'bi-star-fill',
            'color': 'from-yellow-500 to-amber-600',
            'unlocked': watchlist_count >= 5,
            'progress': min(100, (watchlist_count / 5) * 100)
        },
        {
            'id': 'seven_day_streak',
            'name': 'Consistent Tracker',
            'description': 'Maintain 7-day logging streak',
            'icon': 'bi-fire',
            'color': 'from-orange-500 to-red-600',
            'unlocked': streak >= 7,
            'progress': min(100, (streak / 7) * 100)
        }
    ]
    
    # Count unlocked achievements
    unlocked_count = sum(1 for a in achievements_list if a['unlocked'])
    
    return render_template('achievements.html',
                         level=level,
                         level_progress=level_progress,
                         next_level_transactions=next_level_transactions,
                         total_transactions=total_transactions,
                         streak=streak,
                         achievements=achievements_list,
                         unlocked_count=unlocked_count,
                         user_balance=user_balance,
                         savings_rate=savings_rate)
