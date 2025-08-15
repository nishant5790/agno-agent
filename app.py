from flask import Flask, render_template, request, redirect, url_for, session, send_file
from datetime import datetime
from agent.research_agent import DeepResearcherAgent
import markdown
import io

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Change this in production

# --- HOME PAGE ---
@app.route('/', methods=['GET', 'POST'])
def index():
    if 'chat_history' not in session:
        session['chat_history'] = []
    error = None
    full_report = ''
    stage_status = []
    if request.method == 'POST':
        user_input = request.form.get('user_input')
        if user_input:
            try:
                agent = DeepResearcherAgent()
                current_conversation = {
                    'question': user_input,
                    'response': '',
                    'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                }
                # PHASE 1: Researching
                phase1_msg = "🧠 <b>Phase 1: Researching</b> - Finding and extracting relevant information from the web..."
                stage_status.append(phase1_msg)
                # Show spinner and stage status while running
                render_args = dict(chat_history=session.get('chat_history', []), error=error, stage_status=stage_status, running=True)
                # Render the template with running status before starting
                # (Flask does not stream by default, so this is a placeholder for future async/WS)
                research_content = agent.searcher.run(user_input)
                # PHASE 2: Analyzing
                phase2_msg = "🔬 <b>Phase 2: Analyzing</b> - Synthesizing and interpreting the research findings..."
                stage_status.append(phase2_msg)
                analysis = agent.analyst.run(research_content.content)
                # PHASE 3: Writing Report
                phase3_msg = "✍️ <b>Phase 3: Writing Report</b> - Producing a final, polished report..."
                stage_status.append(phase3_msg)
                report_iterator = agent.writer.run(analysis.content, stream=True)
                for chunk in report_iterator:
                    if chunk.content:
                        full_report += chunk.content
                # Render markdown for assistant response
                current_conversation['response'] = markdown.markdown(full_report, extensions=['extra', 'nl2br'])
                session['chat_history'].append(current_conversation)
                session.modified = True
                return render_template('index.html', chat_history=session.get('chat_history', []), error=error, stage_status=None, running=False)
            except Exception as e:
                error = f"An error occurred: {str(e)}"
                return render_template('index.html', chat_history=session.get('chat_history', []), error=error, stage_status=stage_status, running=False)
    return render_template('index.html', chat_history=session.get('chat_history', []), error=error, running=False)

# --- EXPORT CHAT HISTORY ---
@app.route('/export')
def export_chat():
    chat_history = session.get('chat_history', [])
    markdown_content = "# 🔎 Deep Research Agent - Chat History\n\n"
    for i, conversation in enumerate(chat_history, 1):
        markdown_content += f"## {conversation['question']}\n\n"
        markdown_content += f"{conversation['response']}\n\n"
        if i < len(chat_history):
            markdown_content += "---\n\n"
    buf = io.BytesIO()
    buf.write(markdown_content.encode('utf-8'))
    buf.seek(0)
    filename = f"deep_research_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
    return send_file(buf, as_attachment=True, download_name=filename, mimetype='text/markdown')

# --- NEW CHAT ---
@app.route('/new_chat')
def new_chat():
    session['chat_history'] = []
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
