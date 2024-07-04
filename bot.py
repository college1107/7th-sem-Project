from transformers import AutoModelForQuestionAnswering, AutoTokenizer, pipeline
import spacy
nlp_spacy = spacy.load('en_core_web_lg')

def PreProcess(text):
    doc = nlp_spacy(text)
    tokens = [token.text for token in doc if not token.is_punct]
    return ' '.join(tokens)


def QNA(question,context):
    model_name = "deepset/roberta-base-squad2"
    nlp = pipeline('question-answering', model=model_name, tokenizer=model_name,max_answer_len=500)
    QA_input = {
        'question': f'{question}',
        'context': None
    }
    QA_input['context']=PreProcess(context)
    res = nlp(QA_input)
    print(res)
