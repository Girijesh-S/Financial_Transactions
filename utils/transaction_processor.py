import re
from datetime import datetime
import hashlib

class TransactionProcessor:
    def __init__(self):
        self.transactions = []
        self.account_balance = 10000  # Initial balance
        self.users = {
            'user123': {
                'pin': self.hash_pin('1234'),
                'balance': 10000
            }
        }
    
    def hash_pin(self, pin):
        """Hash PIN for security"""
        return hashlib.sha256(pin.encode()).hexdigest()
    
    def classify_intent(self, text):
        """Classify user intent from voice command"""
        text_lower = text.lower()
        
        # Transfer intent
        if any(word in text_lower for word in ['transfer', 'send', 'pay', 'send money']):
            return 'transfer'
        # Balance intent
        elif any(word in text_lower for word in ['balance', 'check balance', 'account balance']):
            return 'balance'
        # Transactions intent
        elif any(word in text_lower for word in ['transaction', 'history', 'statement', 'transactions']):
            return 'transactions'
        # PIN change intent
        elif any(word in text_lower for word in ['pin', 'change pin', 'reset pin', 'update pin']):
            return 'change_pin'
        else:
            return 'unknown'
    
    def extract_transfer_details(self, text):
        """Extract amount and recipient from transfer command"""
        # Pattern for amount extraction
        amount_pattern = r'(\d+)(?:\s*(?:dollars|rupees|rs|inr|\$))?'
        amount_match = re.search(amount_pattern, text)
        
        # Pattern for recipient extraction
        recipient_pattern = r'(?:to|for)\s+([a-zA-Z\s]+)'
        recipient_match = re.search(recipient_pattern, text.lower())
        
        amount = None
        recipient = None
        
        if amount_match:
            amount = float(amount_match.group(1))
        
        if recipient_match:
            recipient = recipient_match.group(1).strip()
        
        return amount, recipient
    
    def extract_pin_from_speech(self, text):
        """Extract PIN digits from spoken text"""
        number_words = {
            'zero': '0', 'one': '1', 'two': '2', 'three': '3', 'four': '4',
            'five': '5', 'six': '6', 'seven': '7', 'eight': '8', 'nine': '9',
            'ten': '10', 'eleven': '11', 'twelve': '12', 'thirteen': '13', 
            'fourteen': '14', 'fifteen': '15', 'sixteen': '16', 'seventeen': '17',
            'eighteen': '18', 'nineteen': '19', 'twenty': '20'
        }
        
        pin_digits = ""
        words = text.lower().split()
        
        for word in words:
            clean_word = word.strip('.,!?')
            if clean_word in number_words:
                pin_digits += number_words[clean_word]
            elif clean_word.isdigit():
                pin_digits += clean_word
        
        return pin_digits
    
    def process_transfer(self, command_text):
        """Process money transfer command"""
        try:
            amount, recipient = self.extract_transfer_details(command_text)
            
            if amount is None or recipient is None:
                return "Could not understand transfer details. Please specify amount and recipient like 'transfer 500 to John'"
            
            if amount > self.account_balance:
                return f"Insufficient funds. Available balance: ₹{self.account_balance}"
            
            # Process transfer
            self.account_balance -= amount
            self.users['user123']['balance'] = self.account_balance
            
            transaction = {
                'date': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'type': 'debit',
                'amount': amount,
                'description': f'Transfer to {recipient}',
                'balance_after': self.account_balance
            }
            self.transactions.append(transaction)
            
            return f"✅ Successfully transferred ₹{amount} to {recipient}. New balance: ₹{self.account_balance}"
            
        except Exception as e:
            return f"❌ Error processing transfer: {str(e)}"
    
    def check_balance(self):
        """Check account balance"""
        return f"💰 Your current account balance is: ₹{self.account_balance}"
    
    def show_transactions(self, count=5):
        """Show recent transactions"""
        recent_txns = self.transactions[-count:] if self.transactions else []
        
        if not recent_txns:
            return "No recent transactions found."
        
        result = f"📋 Last {len(recent_txns)} transactions:\n"
        for txn in recent_txns:
            emoji = "📤" if txn['type'] == 'debit' else "📥"
            result += f"{emoji} {txn['date']} - ₹{txn['amount']} - {txn['description']}\n"
        
        return result
    
    def change_pin_manual(self, old_pin, new_pin):
        """Change user PIN manually"""
        if self.hash_pin(old_pin) == self.users['user123']['pin']:
            self.users['user123']['pin'] = self.hash_pin(new_pin)
            return True
        return False