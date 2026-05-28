"""
Lead Generation Agent - Generates leads for immigration/trucking services
Creates and qualifies leads for monetization
"""

import asyncio
import random
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional
from loguru import logger

class LeadAgent:
    """AI agent that generates and qualifies business leads"""
    
    def __init__(self, config):
        self.config = config
        self.leads_generated = 0
        self.leads_qualified = 0
        self.conversion_rate = 0.0
        
    async def generate_leads(self, count: int = 5) -> List[Dict[str, Any]]:
        """Generate potential leads"""
        leads = []
        
        lead_sources = [
            {"source": "Facebook Ads", "quality": "medium"},
            {"source": "Google Ads", "quality": "high"},
            {"source": "LinkedIn", "quality": "high"},
            {"source": "Instagram", "quality": "medium"},
            {"source": "Referral", "quality": "very_high"},
            {"source": "Organic Search", "quality": "medium"},
        ]
        
        job_types = [
            "Truck Driver - Slovenia",
            "Caregiver - Germany", 
            "Construction Worker - Poland",
            "Restaurant Staff - UAE",
            "IT Professional - Netherlands",
            "Nurse - Ireland"
        ]
        
        countries = ["Pakistan", "India", "Bangladesh", "Philippines", "Nigeria", "Kenya"]
        
        for i in range(count):
            source = random.choice(lead_sources)
            lead = {
                "id": f"lead_{datetime.now().timestamp()}_{random.randint(1000, 9999)}",
                "name": f"Lead_{random.randint(100, 999)}",
                "email": f"lead{random.randint(100, 999)}@example.com",
                "phone": f"+{random.randint(1, 999)}-{random.randint(1000000, 9999999)}",
                "country": random.choice(countries),
                "job_interest": random.choice(job_types),
                "source": source["source"],
                "quality_score": self._calculate_quality_score(source["quality"]),
                "created_at": datetime.now().isoformat(),
                "status": "new",
                "estimated_value": round(random.uniform(100, 2000), 2)
            }
            
            leads.append(lead)
            self.leads_generated += 1
            logger.info(f"Generated lead: {lead['job_interest']} from {lead['source']}")
        
        return leads
    
    def _calculate_quality_score(self, quality: str) -> int:
        """Calculate lead quality score (1-100)"""
        scores = {
            "low": random.randint(20, 40),
            "medium": random.randint(40, 65),
            "high": random.randint(65, 85),
            "very_high": random.randint(85, 100)
        }
        return scores.get(quality, 50)
    
    async def qualify_lead(self, lead: Dict[str, Any]) -> Dict[str, Any]:
        """Qualify a lead through automated screening"""
        # In production, this would use AI to analyze lead responses
        qualification_questions = [
            "Are you ready to relocate within 3 months?",
            "Do you have a valid passport?",
            "What is your budget for visa processing?",
            "Do you have relevant work experience?",
            "Are you willing to undergo medical testing?"
        ]
        
        # Simulate qualification
        answers_count = random.randint(3, 5)
        qualified = answers_count >= 4
        
        lead["qualified"] = qualified
        lead["qualification_date"] = datetime.now().isoformat()
        lead["answers_count"] = answers_count
        lead["status"] = "qualified" if qualified else "not_qualified"
        
        if qualified:
            self.leads_qualified += 1
            logger.info(f"Lead qualified: {lead['id']} - Value: ${lead['estimated_value']}")
        else:
            logger.warning(f"Lead not qualified: {lead['id']}")
        
        return lead
    
    async def nurture_leads(self, leads: List[Dict[str, Any]]) -> Dict[str, int]:
        """Send follow-up messages to nurture leads"""
        results = {"contacted": 0, "responded": 0, "converted": 0}
        
        message_templates = [
            "Hi! We noticed you're interested in {job}. Would you like to schedule a free consultation?",
            "Great news! We have new opportunities for {job} in Europe. Interested?",
            "Quick question: Are you still looking for overseas employment opportunities?",
        ]
        
        for lead in leads:
            if lead["status"] == "new" or lead["status"] == "qualified":
                # Simulate sending message
                results["contacted"] += 1
                
                # Simulate response
                if random.random() < 0.4:  # 40% response rate
                    results["responded"] += 1
                    
                    # Simulate conversion
                    if random.random() < 0.25:  # 25% conversion from responses
                        results["converted"] += 1
                        lead["status"] = "converted"
                        logger.info(f"Lead converted: {lead['id']}")
        
        return results
    
    async def send_to_crm(self, lead: Dict[str, Any]) -> bool:
        """Send qualified lead to CRM system"""
        # In production, this would integrate with HubSpot, Salesforce, etc.
        logger.info(f"Sending lead to CRM: {lead['id']}")
        await asyncio.sleep(0.2)  # Simulate API call
        return True
    
    async def get_lead_analytics(self) -> Dict[str, Any]:
        """Get analytics on lead generation performance"""
        return {
            "total_leads": self.leads_generated,
            "qualified_leads": self.leads_qualified,
            "conversion_rate": round((self.leads_qualified / max(self.leads_generated, 1)) * 100, 2),
            "average_lead_value": round(random.uniform(300, 800), 2),
            "top_source": "Google Ads",
            "top_job_type": "Truck Driver - Slovenia"
        }
