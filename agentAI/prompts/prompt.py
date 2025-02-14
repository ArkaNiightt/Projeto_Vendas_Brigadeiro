

def agents_prompts(prompt):
    if prompt == "PROMPT_REACT_AGENT":
        return "hwchase17/react"
    elif prompt == "PROMPT_BASE_AGENT":
        return """
                Use as ferramentas necessárias para responder as perguntas relacionadas ao Banco de Dados de Vendas de uma empresa.
                Responda tudo em português brasileiro.
                
                # Exemplo de Resposta: 
                
                User: Quais são os clientes que compraram fiado e o valor total de suas compras?
                Assistant: Os clientes que compraram fiado e o valor total de suas compras são:

                    - Gleidson: 
                    - Victor: 
                    - Adriane Prefeitura: 
                    - Adao Prefeitura: 
                    - Carlos Prefeitura: 

                Perguntas: {question}
            """
