"""
Database module for storing conversation history
"""
from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
import json

Base = declarative_base()

class Conversation(Base):
    __tablename__ = 'conversations'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(200))
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    model = Column(String(100))
    messages_json = Column(Text)  # Store messages as JSON
    message_count = Column(Integer, default=0)

class Database:
    def __init__(self, db_path="conversations.db"):
        self.engine = create_engine(f'sqlite:///{db_path}')
        Base.metadata.create_all(self.engine)
        Session = sessionmaker(bind=self.engine)
        self.session = Session()
    
    def create_conversation(self, title, model):
        """Create a new conversation"""
        conv = Conversation(
            title=title,
            model=model,
            messages_json=json.dumps([]),
            message_count=0
        )
        self.session.add(conv)
        self.session.commit()
        return conv.id
    
    def update_conversation(self, conv_id, messages):
        """Update conversation with new messages"""
        conv = self.session.query(Conversation).filter_by(id=conv_id).first()
        if conv:
            conv.messages_json = json.dumps(messages)
            conv.message_count = len(messages)
            conv.updated_at = datetime.utcnow()
            self.session.commit()
            return True
        return False
    
    def get_conversation(self, conv_id):
        """Get a specific conversation"""
        conv = self.session.query(Conversation).filter_by(id=conv_id).first()
        if conv:
            return {
                'id': conv.id,
                'title': conv.title,
                'created_at': conv.created_at,
                'updated_at': conv.updated_at,
                'model': conv.model,
                'messages': json.loads(conv.messages_json),
                'message_count': conv.message_count
            }
        return None
    
    def get_all_conversations(self):
        """Get all conversations, sorted by most recent"""
        convs = self.session.query(Conversation).order_by(Conversation.updated_at.desc()).all()
        return [{
            'id': c.id,
            'title': c.title,
            'created_at': c.created_at,
            'updated_at': c.updated_at,
            'model': c.model,
            'message_count': c.message_count
        } for c in convs]
    
    def delete_conversation(self, conv_id):
        """Delete a conversation"""
        conv = self.session.query(Conversation).filter_by(id=conv_id).first()
        if conv:
            self.session.delete(conv)
            self.session.commit()
            return True
        return False
    
    def search_conversations(self, query):
        """Search conversations by title or content"""
        convs = self.session.query(Conversation).filter(
            (Conversation.title.contains(query)) | 
            (Conversation.messages_json.contains(query))
        ).order_by(Conversation.updated_at.desc()).all()
        
        return [{
            'id': c.id,
            'title': c.title,
            'created_at': c.created_at,
            'updated_at': c.updated_at,
            'model': c.model,
            'message_count': c.message_count
        } for c in convs]
