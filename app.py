# app.py
# Milestone 5 — Gradio Web Interface
# Provides a web UI for querying the weight loss RAG system.

import gradio as gr
from generate import generate, all_chunks
from embed import retrieve

def handle_query(question):
    if not question.strip():
        return "Please enter a question.", ""

    # Check for out-of-scope queries
    weight_loss_keywords = [
        "weight", "calorie", "diet", "exercise", "protein", "fat", "sleep",
        "stress", "metabolism", "food", "eat", "nutrition", "fitness", "health",
        "workout", "cardio", "muscle", "plateau", "deficit", "loss", "gain"
    ]

    question_lower = question.lower()
    is_relevant = any(word in question_lower for word in weight_loss_keywords)

    if not is_relevant:
        return (
            "I can only answer questions related to weight loss and healthy living. "
            "Please ask a question about topics such as calorie deficits, exercise, "
            "nutrition, sleep, or metabolism."
        ), ""

    # Retrieve top-3 chunks and get sources
    chunks = retrieve(question, k=3)
    answer = generate(question)

    # Format sources
    seen = set()
    source_lines = []
    for chunk in chunks:
        key = chunk["source"]
        if key not in seen:
            seen.add(key)
            source_lines.append(f"• {chunk['source']} — {chunk['url']}")

    sources = "\n".join(source_lines) if source_lines else "No sources found."

    return answer, sources


with gr.Blocks(title="Weight Loss Unofficial Guide") as demo:
    gr.Markdown("# 🥗 Weight Loss Unofficial Guide")
    gr.Markdown(
        "Ask any evidence-based question about weight loss, nutrition, exercise, "
        "sleep, or metabolism. Answers are grounded in verified sources."
    )

    with gr.Row():
        with gr.Column():
            question_input = gr.Textbox(
                label="Your question",
                placeholder="e.g. What is a calorie deficit and why does it matter?",
                lines=2
            )
            ask_btn = gr.Button("Ask", variant="primary")

        with gr.Column():
            answer_output = gr.Textbox(
                label="Answer",
                lines=10
            )
            sources_output = gr.Textbox(
                label="Sources",
                lines=4
            )

    ask_btn.click(
        handle_query,
        inputs=question_input,
        outputs=[answer_output, sources_output]
    )
    question_input.submit(
        handle_query,
        inputs=question_input,
        outputs=[answer_output, sources_output]
    )

    gr.Markdown("### Example questions to try:")
    gr.Markdown(
        "- What is a calorie deficit and why is it important for weight loss?\n"
        "- How much weight loss per week is considered safe?\n"
        "- Why is protein important during weight loss?\n"
        "- How does sleep affect weight loss?\n"
        "- What causes a weight loss plateau and how can it be overcome?"
    )

demo.launch()
