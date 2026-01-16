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
                "You are an expert CV writer and career advisor. "
                "Your task is to tailor the provided CV to match the given job description."
                "{format_instructions}\n"
                "You will be provided with the current CV and a job seeker story."
                "Use only the information from these sources for the output data—do not fabricate or add information not present in the provided materials."
                "Instructions:\n"
                "1. Analyze the job description carefully to understand the key requirements, skills, and qualifications\n"
                "2. Modify the CV content to emphasize relevant experience and skills\n"
                "3. Rewrite bullet points to highlight achievements that match the job requirements\n"
                "4. Use keywords from the job description naturally throughout the CV\n"
                "5. Maintain professionalism and truthfulness - do not add fake information\n"
                "6. Keep the same writing style but optimize the content for this specific role\n"
                "Here is the job description:\n"
                "{job_description}\n"
                "Here is the base CV in JSON format:\n"
                "{base_cv}\n"
                "Here is the user story to consider:\n"
                "{user_story}\n"
            ),
            input_variables=["user_story", "job_description", "base_cv"],
            partial_variables={
                "format_instructions": self.cv_generator_parser.get_format_instructions()
            },
        )
        self.cv_generator_chain = (
            self.cv_generator_prompt | self.model | self.cv_generator_parser
        )

    def generate_cv(self, user_story: str, job_description: str, base_cv: CV) -> CV:
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
