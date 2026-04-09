import os
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from dotenv import load_dotenv

load_dotenv()

class Brain:
    def __init__(self):
        # Using the Pro model for stability and higher limits
        self.llm = ChatGoogleGenerativeAI(
            model="gemini-pro-latest",
            temperature=0.3,
            api_key=os.getenv("GEMINI_API_KEY")
        )
        
        # COMPETITION REQUIREMENT: Contextual Real Estate Persona
        self.prompt = ChatPromptTemplate.from_template(
            """
            You are "Omni", a professional Real Estate Support Agent for a top builder.
            
            YOUR GOAL: Build a customer profile by naturally asking these 4 questions (one at a time):
            1. Where do they currently stay?
            2. What are they looking for? (Apartment, Villa, Plot)
            3. What is their budget?
            4. When do they plan to move?

            RULES:
            - Keep answers short (max 2 sentences).
            - Be polite but professional.
            - Logic: If they are in NCR, suggest Noida or Gurgaon. 
            - Logic: If they want a "Villa", do not offer Apartments.
            - Once you have the info, thank them and say an agent will call back.

            Current conversation:
            {history}
            
            User: {input}
            AI:
            """
        )
        self.history = []

    async def think(self, text):
        # Format the conversation history
        history_text = "\n".join(self.history[-5:]) 
        
        chain = self.prompt | self.llm
        response = await chain.ainvoke({"input": text, "history": history_text})
        
        # Cleanup response
        answer = response.content
        if isinstance(answer, list) and len(answer) > 0:
            if isinstance(answer[0], dict):
                answer = answer[0].get("text", "")
            else:
                answer = str(answer[0])
        else:
            answer = str(answer)
        
        # Save to short-term memory
        self.history.append(f"User: {text}")
        self.history.append(f"AI: {answer}")
        
        return answer

    # COMPETITION REQUIREMENT: Module B (Automated MoM)
    async def generate_mom(self, full_conversation):
        print("📝 Generating Minutes of Meeting...")
        
        transcript = "\n".join(full_conversation)
        
        mom_prompt = f"""
        Analyze this sales call and produce a structured 'Minutes of Meeting'.
        
        TRANSCRIPT:
        {transcript}
        
        OUTPUT FORMAT:
        1. Customer Intent: (Buying/Selling/Inquiry)
        2. Location Preference:
        3. Budget:
        4. Property Type:
        5. Timeline:
        6. Follow-up Action:
        """
        
        try:
            response = await self.llm.ainvoke(mom_prompt)
            return response.content
        except Exception as e:
            return f"Error generating MoM: {e}"