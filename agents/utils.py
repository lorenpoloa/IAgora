from transformers import pipeline
import ollama

""" def generate_response(agent, topic, previous_posts):
    print(f"TESTING: Topic {topic.title}")            

    context = f"Topic: {topic.title}\nDescription: {topic.description}\n\nPrevious posts:\n"
    for post in previous_posts:
        context += f"{post.author.name}: {post.content}\n"

    context += f"\n{agent.name}'s turn to respond. {agent.context_of_behavior}\n"

    if agent.model_architecture == 'other':
        try:
            
            print(f"Ollama generating response for model: {agent.checkpoint}")            
            response = ollama.generate(model="gemma3:1b", prompt=context)
            return response['response'].strip()
        except Exception as e:
            print(f"Ollama error: {e}")
            return "Error generating response with Ollama."
    else:
        try:
            generator = pipeline('text-generation', model=agent.checkpoint)
            response = generator(context, max_length=500, num_return_sequences=1)[0]['generated_text']
            return response.strip()
        except Exception as e:
            print(f"Transformers error: {e}")
            return "Error generating response with Transformers." """



def generate_response(agent, topic, previous_posts):
    print(f"TESTING: Topic {topic.title}")

    # Mensajes que se mandarán a Ollama
    messages = []

    # Contexto del agente en el rol "system"
    # Esto es importante para que el agente sepa cómo comportarse
    messages.append({
        "role": "system",
        "content": f"{agent.context_of_behavior}\n\nIMPORTANT: Do not include <think> or hidden reasoning in your response. Only return the final answer."
    })

    # Contexto del tema y descripción
    messages.append({
        'role': 'user',
        'content': f"{topic.title}\n{topic.description}\n"
    })

    # Agregar los posts previos
    for post in previous_posts:
        # Si el autor es el agente, lo marcamos como "assistant"
        role = "assistant" if post.author.name == agent.name else "user"
        
        messages.append({
            'role': role,
            'content': f"Author: {post.author.name}. Post: {post.content}"
        })

    # Generación con Ollama solo si es modelo 'other'
    if agent.model_architecture == "other":
        try:
            print(f"Ollama generating response for model: {agent.name}")
            response = ollama.chat(
                model=agent.name,   # <-- agent.name should match the Ollama model name
                messages=messages
            )
            # Retornar el contenido de la respuesta
            return response["message"]["content"].strip()
        
        except Exception as e:
            print(f"Ollama error: {e}")
            return "Error generating response with Ollama."
    else:
        return f"Agent {agent.name} no está configurado para usar Ollama."
