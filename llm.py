from typing import Literal
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
        self.__init_cv_generator()

    def __init_cv_parser(self):
        self.cv_parser = PydanticOutputParser(pydantic_object=CVWithPersonalInfo)
        self.cv_parser_prompt = PromptTemplate(
            template=(
                "You are an expert CV parser."
                "Extract all information from the following CV text into the requested JSON format.\n"
                "{format_instructions}"
                "CV Text:\n"
                "{raw_cv_text}"
            ),
            input_variables=["raw_cv_text"],
            partial_variables={
                "format_instructions": self.cv_parser.get_format_instructions()
            },
        )
        self.cv_parser_chain = self.cv_parser_prompt | self.model | self.cv_parser

    def __init_cv_generator(self):
        self.cv_generator_parser = PydanticOutputParser(pydantic_object=CV)
        self.cv_generator_prompt = PromptTemplate(
            template=(
                "You are an expert CV generator."
                "Based on the job seeker story, job description, and base CV provided,"
                "generate a tailored CV in the requested JSON format.\n"
                "{format_instructions}\n"
                "Job Seeker Story:\n"
                "{user_story}\n\n"
                "Job Description:\n"
                "{job_description}\n\n"
                "Base CV:\n"
                "{base_cv}"
            ),
            input_variables=["user_story", "job_description", "base_cv"],
            partial_variables={
                "format_instructions": self.cv_generator_parser.get_format_instructions()
            },
        )
        self.cv_generator_chain = (
            self.cv_generator_prompt | self.model | self.cv_generator_parser
        )

    def generate_cv(
        self, user_story: str, job_description: str, base_cv: CV
    ) -> CV:
        response = self.cv_generator_chain.invoke(
            {
                "user_story": user_story,
                "job_description": job_description,
                "base_cv": base_cv.model_dump_json(),
            }
        )

        return response

    def parse_cv_with_personal_info(self, raw_cv_path) -> CVWithPersonalInfo:

        loader = PyPDFLoader(raw_cv_path)

        docs = loader.load_and_split()
        # load hypertext links if any

        raw_cv_text = "\n".join([doc.page_content for doc in docs])

        parsed_cv = self.cv_parser_chain.invoke({"raw_cv_text": raw_cv_text})
        # TODO do fuzzy matching to link url_annotations to parsed_cv.links
        # get url by reading all annotations from pdf

        return parsed_cv


if __name__ == "__main__":
    llm = LLM(provider="ollama")
    print("LLM initialized successfully.")

    parsed_cv = llm.parse_cv_with_personal_info("temp/cv.pdf")
    # save the parsed cv as json
    import json

    with open("temp/parsed_cv.json", "w", encoding="utf-8") as f:
        json.dump(parsed_cv.model_dump(), f, ensure_ascii=False, indent=4)
