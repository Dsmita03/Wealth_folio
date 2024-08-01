
# Importing services to make them available at the package level
from .budget_service import BudgetService
from .goal_service import GoalService
from .notification_service import NotificationService
from .receipt_service import ReceiptService
from .transaction_service import TransactionService
from .ml_service import MLService
from .reminder_service import ReminderService
from .bill_service import BillService


class Config:
    SQLALCHEMY_DATABASE_URI = 'mysql+mysqlconnector://debasmita:12345@100.122.226.52.3306/wealthapp'
    SQLALCHEMY_TRACK_MODIFICATIONS = False