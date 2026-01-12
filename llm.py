from typing import Literal
from langchain_core.messages import HumanMessage, SystemMessage
from models import CV, CVWithPersonalInfo
from langchain_community.document_loaders import PyPDFLoader
from langchain_core.output_parsers import PydanticOutputParser
from langchain_core.prompts import PromptTemplate


class LLM:
    def __init__(self, provider: Literal["ollama"] = "ollama"):
        if provider == "ollama":
            from langchain_ollama import ChatOllama

            self.model = ChatOllama(
                model="deepseek-r1:14b",
                temperature=0.1,
                validate_model_on_init=True,
                num_predict=4096,
            )
        # elif provider == "openai":
        #     try:
        #         from langchain_openai import ChatOpenAI
        #     except ImportError:
        #         raise ImportError(
        #             "langchain_openai is not installed. Please install it with 'uv add '"
        #         )
        #     self.model = ChatOpenAI(
        #         model_name="gpt-4",
        #         temperature=0.2,
        #     )
        else:
            raise ValueError(f"Unsupported LLM provider: {provider}")

        self.__init_cv_parser()

        self.cv_generator_structured_llm = self.model.with_structured_output(CV)

    def __init_cv_parser(self):
        self.cv_parser = PydanticOutputParser(pydantic_object=CVWithPersonalInfo)
        self.cv_parser_prompt = PromptTemplate(
            template="""You are an expert CV parser. 
    Extract all information from the following CV text into the requested JSON format.
    
    {format_instructions}
    
    CV Text:
    {raw_cv_text}
    """,
            input_variables=["raw_cv_text"],
            partial_variables={
                "format_instructions": self.cv_parser.get_format_instructions()
            },
        )
        self.cv_parser_chain = self.cv_parser_prompt | self.model | self.cv_parser

    def generate_cv(
        self, system_prompt: str, user_story: str, job_description: str, base_cv: CV
    ) -> CV:
        messages = [
            SystemMessage(content=system_prompt),
            HumanMessage(
                content=(
                    f"Here is the job seeker story:\n{user_story}\n\n"
                    f"Here is the job description:\n{job_description}\n\n"
                    f"Here is the base CV:\n{base_cv}\n\n"
                    "Generate a tailored CV based on the above information."
                )
            ),
        ]

        response = self.cv_generator_structured_llm.invoke(messages)

        return response  # type: ignore

    def parse_cv_with_personal_info(self, raw_cv_path) -> CVWithPersonalInfo:

        loader = PyPDFLoader(raw_cv_path)

        docs = loader.load_and_split()

        raw_cv_text = "\n".join([doc.page_content for doc in docs])

        parsed_cv = self.cv_parser_chain.invoke({"raw_cv_text": raw_cv_text})

        return parsed_cv


if __name__ == "__main__":
    llm = LLM(provider="ollama")
    print("LLM initialized successfully.")

    parsed_cv = llm.parse_cv_with_personal_info("temp/cv.pdf")
    # save the parsed cv as json
    import json

    with open("temp/parsed_cv.json", "w", encoding="utf-8") as f:
        json.dump(parsed_cv.model_dump(), f, ensure_ascii=False, indent=4)
