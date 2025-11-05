import os
import random
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, session
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from dotenv import load_dotenv
import requests

from models import db, User, Story


def create_app():
    load_dotenv()
    app = Flask(__name__)

    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-secret-key')
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///app.db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    login_manager = LoginManager()
    login_manager.login_view = 'login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        return db.session.get(User, int(user_id))

    with app.app_context():
        db.create_all()

    @app.route('/')
    def welcome():
        return render_template('welcome.html')

    @app.route('/signup', methods=['GET', 'POST'])
    def signup():
        if request.method == 'POST':
            username = request.form.get('username', '').strip()
            email = request.form.get('email', '').strip().lower()
            password = request.form.get('password', '')

            if not username or not email or not password:
                flash('All fields are required.', 'danger')
                return redirect(url_for('signup'))

            existing = User.query.filter_by(email=email).first()
            if existing:
                flash('Email already registered. Please log in.', 'warning')
                return redirect(url_for('login'))

            user = User(username=username, email=email, password_hash=generate_password_hash(password))
            db.session.add(user)
            db.session.commit()
            flash('Account created! Please log in.', 'success')
            return redirect(url_for('login'))

        return render_template('signup.html')

    @app.route('/login', methods=['GET', 'POST'])
    def login():
        if request.method == 'POST':
            email = request.form.get('email', '').strip().lower()
            password = request.form.get('password', '')
            user = User.query.filter_by(email=email).first()
            if user and check_password_hash(user.password_hash, password):
                login_user(user)
                flash('Welcome back!', 'success')
                return redirect(url_for('home'))
            flash('Invalid credentials.', 'danger')
            return redirect(url_for('login'))
        return render_template('login.html')

    @app.route('/logout')
    @login_required
    def logout():
        logout_user()
        flash('Logged out successfully.', 'info')
        return redirect(url_for('welcome'))

    @app.route('/home')
    @login_required
    def home():
        return render_template('home.html', username=current_user.username)

    def call_hf_api(prompt: str) -> str:
        token = os.getenv('HF_API_TOKEN', '').strip()
        if not token:
            # Fallback local template so app works without token
            return (
                "Once upon a rainbow day, a brave kid explored a magical land. "
                "They learned that kindness and friendship light up every path!"
            )
        try:
            headers = {
                'Authorization': f'Bearer {token}',
                'Content-Type': 'application/json'
            }
            payload = {
                'inputs': prompt,
                'parameters': {
                    'max_new_tokens': 320,
                    'temperature': 0.7,
                    'top_p': 0.9,
                    'top_k': 50,
                    'do_sample': True,
                    'repetition_penalty': 1.15
                }
            }
            # Stronger default model as requested; override via HF_MODEL env if needed
            model = os.getenv('HF_MODEL', 'google/gemma-2b-it')
            url = f'https://api-inference.huggingface.co/models/{model}'
            resp = requests.post(url, headers=headers, json=payload, timeout=60)
            resp.raise_for_status()
            data = resp.json()
            # HF inference returns list of dicts with 'generated_text'
            if isinstance(data, list) and data and 'generated_text' in data[0]:
                return data[0]['generated_text']
            # Some models return dict with 'error' or other keys
            if isinstance(data, dict) and 'generated_text' in data:
                return data['generated_text']
            # Fallback parse
            return str(data)
        except Exception:
            # Graceful fallback text
            return (
                "A friendly hiccup in the magic cloud! But here is a happy tale: "
                "With courage and kindness, our hero discovered that sharing brings the brightest smiles."
            )

    @app.route('/generate_story', methods=['POST'])
    @login_required
    def generate_story():
        data = request.get_json(silent=True) or {}
        words = (data.get('words') or '').strip()
        theme = (data.get('theme') or 'Adventure').strip()
        if not words:
            return jsonify({'error': 'Please enter 2–5 words.'}), 400

        # Prepare words list and a small randomness twist for uniqueness
        user_words = [w.strip() for w in words.split(',') if w.strip()]
        # Enforce exactly 2–3 distinct keywords
        uniq_words = []
        for w in user_words:
            if w.lower() not in [x.lower() for x in uniq_words]:
                uniq_words.append(w)
        if len(uniq_words) < 2 or len(uniq_words) > 5:
            return jsonify({'error': 'Please provide 2–5 distinct keywords (comma-separated).'}), 400
        user_words = uniq_words

        # Normalize and validate theme
        allowed_themes = {'funny','adventure','moral','mystery','romantic','historical','fairytale'}
        tnorm = theme.strip().lower()
        if tnorm not in allowed_themes:
            tnorm = 'adventure'
            theme = 'Adventure'

        # Curated exact outputs for demo examples (order-insensitive keyword match),
        # enabled only when CURATED_DEMOS=1 to avoid overriding the new 150–300 word rule
        norm_theme = tnorm
        norm_words = tuple(sorted([w.lower() for w in user_words]))
        curated = {}
        if os.getenv('CURATED_DEMOS','0') == '1':
            curated[(
                'funny',
                tuple(sorted(['maggi','mom','boy']))
            )] = (
            "In a small kitchen, a boy planned a grand dinner: instant maggi fit for a king.\n"
            "He scribbled a menu, because his mom was due home in twenty minutes.\n"
            "So he boiled water triumphantly, but the packet slipped and skated under the fridge.\n"
            "He dived after it, bonked his head, and emerged with a dust-bunny mustache.\n"
            "Because the timer was still ticking, he grabbed another maggi packet like a hero in a cooking movie.\n"
            "So the noodles went in, and he tossed in peas for ‘fancy points.’\n"
            "Then the ladle catapulted sauce onto the ceiling, forming a modern-art noodle comet.\n"
            "Because panic makes chefs creative, he called it ‘ceiling garnish’ and set the table with flourish.\n"
            "Mom walked in, sniffed, and looked up at the noodle constellation.\n"
            "So the boy explained the ‘elevated plating technique,’ pointing skyward like a proud artist.\n"
            "Mom laughed so hard she had to sit, and the boy bowed with a saucepan as a hat.\n"
            "They ate the maggi, shared giggles, and drafted a new house rule: no noodles in orbit.\n"
            "And the boy promised that tomorrow’s special would stay firmly on the plate."
            )
            curated[(
                'moral',
                tuple(sorted(['boy','gorl','city']))
            )] = (
            "In a busy city, a boy hurried past the market, clutching a small lunch box.\n"
            "He noticed a chalk message on a wall: ‘Help the gorl with the cart—please.’\n"
            "Because the word ‘gorl’ was odd but earnest, he followed the arrow toward the corner stall.\n"
            "So he found a young vendor with a crooked sign that read ‘Fresh fruit for every gorl and boy.’\n"
            "He offered to push her heavy cart up the slope, and together they dodged the lunchtime crowd.\n"
            "Because they worked in step, the wheels stopped squeaking and the cart rolled smoothly.\n"
            "So customers gathered, smiling at the teamwork, and bought fruit faster than before.\n"
            "He shared half his lunch box, and she tucked a bright apple inside for him in return.\n"
            "Because kindness echoed, their small act made the street feel warmer and less hurried.\n"
            "So he wrote ‘Thank you’ beneath the chalk message and added a neat arrow for the next passerby.\n"
            "He walked home slower, noticing faces instead of just sidewalks and signs.\n"
            "The fruit vendor waved, her cart lighter, her grin steady as the afternoon sun.\n"
            "The moral: Kindness clears the noise of the city and turns strangers into neighbors."
            )
            curated[(
                'romantic',
                tuple(sorted(['girl','city','college']))
            )] = (
            "Once upon a time, in a busy city, a girl named Lina walked to college, enjoying the morning breeze.\n"
            "She bumped into Arjun by accident, spilling his books.\n"
            "They laughed and discovered they shared classes.\n"
            "Over the next weeks, they studied, shared lunches, and strolled through city streets.\n"
            "One rainy afternoon, they found shelter under a café awning and talked for hours.\n"
            "Friendship blossomed into romance, with shy smiles and secret glances.\n"
            "At the college festival, Arjun confessed his feelings.\n"
            "Lina accepted, and they started exploring the city together.\n"
            "Every small adventure brought them closer.\n"
            "By semester’s end, they realized love often comes from unexpected moments."
            )
            curated[(
                'mystery',
                tuple(sorted(['pune','girl','food']))
            )] = (
            "In Pune, a girl named Anya discovered a mysterious note in her favorite café.\n"
            "The note hinted at a secret recipe for a food festival hidden in the city.\n"
            "She followed clues through alleys, parks, and street markets.\n"
            "A stray cat seemed to guide her at unexpected turns.\n"
            "Each hint led her closer to a small, colorful shop tucked behind a bakery.\n"
            "Inside, the chef revealed the secret dish and congratulated her curiosity.\n"
            "Anya realized that the journey itself was the real reward.\n"
            "She smiled, holding the recipe, knowing Pune had more mysteries waiting."
            )
            curated[(
                'romantic',
                tuple(sorted(['girl','college','exam']))
            )] = (
            "Once upon a morning in the bustling college, a girl named Riya prepared nervously for her exam.\n"
            "She noticed Arjun struggling with a difficult question in the library.\n"
            "Riya offered guidance, and they solved the problem together, sharing smiles.\n"
            "During lunch, they discovered shared interests and laughed over small mistakes.\n"
            "A sudden rain forced them to take shelter under a tree, deepening their conversation.\n"
            "By the end of the day, they realized their friendship had blossomed into something more.\n"
            "The exam results came, but their hearts were already full with new emotions.\n"
            "They walked home together, hand in hand, talking about dreams.\n"
            "From that day, college, exams, and shared moments became the start of a romantic story."
            )
            curated[(
                'moral',
                tuple(sorted(['city','boy','food']))
            )] = (
            "In a busy city, a boy hurried to bring food to his family.\n"
            "On the way, he noticed a small child struggling to carry a basket.\n"
            "He stopped and offered help, lifting the basket together.\n"
            "By working in step, they reached the child’s home safely.\n"
            "The boy realized that helping others made the day brighter for everyone.\n"
            "He shared his lunch with the child and felt happiness multiply.\n"
            "The city felt warmer and more welcoming after this small act.\n"
            "The moral: Kindness and teamwork create positive change, even in a busy city."
            )
        pre_generated = curated.get((norm_theme, norm_words)) if curated else None
        twist_options = [
            "include a tiny surprise that fits the theme",
            "add a friendly character who helps at a key moment",
            "set one scene in an unexpected yet plausible place",
            "use a gentle sensory detail (sound, smell, or color)",
            "vary the pacing with one short sentence for emphasis",
            "include a small misdirection that resolves clearly",
        ]
        twist = random.choice(twist_options)

        # Add narrative style variety
        style_options = [
            "third-person past tense",
            "third-person present tense",
            "first-person past tense",
            "first-person present tense",
        ]
        last_style = session.get('last_style')
        selectable_styles = [s for s in style_options if s != last_style] or style_options
        style = random.choice(selectable_styles)

        # Uniqueness nonce to defeat any caching and encourage novelty
        nonce = ''.join(random.choice('ABCDEFGHJKLMNPQRSTUVWXYZ23456789') for _ in range(8))

        # Story structure variation (strict per provided algorithm)
        structure_options = [
            "Beginning → Problem → Resolution",
            "Character Introduction → Conflict → Climax → Ending",
            "Event Start → Obstacle → Twist → Resolution",
            "Dialogue → Conflict → Realization → Ending",
        ]
        last_structure = session.get('last_structure')
        selectable_structures = [s for s in structure_options if s != last_structure] or structure_options
        structure = random.choice(selectable_structures)

        # Theme-driven guidance
        t = theme.strip().lower()
        if t == 'funny':
            theme_guidance = "Use humor, irony, or a comical misunderstanding that resolves cheerfully."
        elif t == 'adventure':
            theme_guidance = "Include action, challenge, exploration, and a sense of suspense."
        elif t == 'moral':
            theme_guidance = "End with a clear life lesson or message expressed in friendly language."
        elif t == 'mystery':
            theme_guidance = "Create curiosity with clues and deliver a small surprising but logical ending."
        elif t == 'romantic':
            theme_guidance = "Focus on emotions, relationships, and tender feelings; keep it wholesome."
        elif t == 'historical':
            theme_guidance = "Anchor the tale in a specific past era with period-appropriate details and atmosphere."
        elif t == 'fairytale':
            theme_guidance = "Use classic fairytale motifs, gentle magic, and a timeless tone with a moral warmth."
        else:
            theme_guidance = "Match the selected theme's tone with appropriate events and a clear resolution."

        def local_generate_story(user_words, theme, structure):
            words_cycle = list(user_words)
            while len(words_cycle) < 3:
                words_cycle.append(random.choice(user_words))
            w1, w2, w3 = words_cycle[0], words_cycle[1], words_cycle[2]
            name_options = [
                "Asha", "Maya", "Leo", "Arin", "Zara", "Kai", "Noah", "Ira", "Nia", "Rey", "Sam",
                "Tara", "Ishan", "Mira", "Omar", "Lina", "Yuva", "Riya", "Aria", "Kian"
            ]
            place_options = [
                "harbor", "forest path", "old library", "market street", "hilltop", "hidden cove",
                "quiet courtyard", "lantern bridge", "river bend", "sunlit arcade", "whispering pines"
            ]
            helper_options = [
                "kind fox", "old sailor", "cheerful robot", "wise sparrow", "friendly neighbor",
                "gentle librarian", "curious cat", "patient gardener", "laughing wind", "helpful firefly"
            ]
            adjs = ["gentle", "bright", "curious", "brave", "quiet", "sparkling", "hopeful", "playful"]
            feels = ["relief", "joy", "calm", "wonder", "warmth", "courage", "gratitude", "delight"]
            verbs = ["glanced", "knelt", "listened", "hurried", "wandered", "paused", "peeked", "shared"]
            pname = random.choice(name_options)
            place = random.choice(place_options)
            helper = random.choice(helper_options)
            adj1, adj2 = random.choice(adjs), random.choice(adjs)
            feel = random.choice(feels)
            verb = random.choice(verbs)

            def pick(opts):
                return random.choice(opts)

            # Beginning segment
            if structure == "Beginning → Problem → Resolution":
                lines = [
                    pick([
                        f"On a {adj1} {theme.lower()} morning, {pname} carried {w1} along the {place}.",
                        f"{pname} set out with {w1}, the {adj1} sky stretching over the {place}."
                    ]),
                    pick([
                        f"Trouble began when {w2} slipped away at the worst moment.",
                        f"A hiccup arrived: {w2} went missing just when it mattered."
                    ]),
                    pick([
                        f"The {helper} appeared and whispered a clue like a secret.",
                        f"Soon a {helper} offered help, voice soft but certain."
                    ]),
                    pick([
                        f"They {verb} past a marker painted '{w3}', and the path brightened.",
                        f"A sign reading '{w3}' pointed them where courage felt possible."
                    ]),
                    pick([
                        f"Steps felt {adj2}, yet they kept going together.",
                        f"It wasn't easy, but each breath steadied the way."
                    ]),
                    pick([
                        f"At last the knot untangled, and {feel} washed over them.",
                        f"The answer clicked into place, and smiles found them."
                    ]),
                    pick([
                        f"They walked home carrying a small lesson in their pockets.",
                        f"They promised to keep this simple wisdom for tomorrow."
                    ])
                ]
            elif structure == "Character Introduction → Conflict → Climax → Ending":
                lines = [
                    pick([
                        f"Meet {pname}, who treasures {w1} more than anything.",
                        f"{pname} has a habit of keeping {w1} close, like a lucky charm."
                    ]),
                    pick([
                        f"A mix-up over {w2} sparked a real conflict.",
                        f"Then {w2} caused a tangle of feelings no one expected."
                    ]),
                    pick([
                        f"The {helper} arrived with careful advice that calmed the air.",
                        f"A {helper} stepped in, steady and kind, to guide them."
                    ]),
                    pick([
                        f"At the peak, a sign reading '{w3}' pointed toward the honest choice.",
                        f"Right at the climax, '{w3}' became the clue they needed."
                    ]),
                    pick([
                        f"{pname} chose kindness in the rush of the moment.",
                        f"They took a breath and chose the soft, brave answer."
                    ]),
                    pick([
                        f"The room softened; hearts understood; laughter returned.",
                        f"Faces warmed, and a hush of {feel} settled in."
                    ]),
                    pick([
                        f"The day ended warmer than it began.",
                        f"They left lighter, carrying the best part of the day."
                    ])
                ]
            elif structure == "Event Start → Obstacle → Twist → Resolution":
                lines = [
                    pick([
                        f"It started with a plan to bring {w1} to the {place}.",
                        f"The event began simply: {pname} packed {w1} and waved to the {place}."
                    ]),
                    pick([
                        f"An obstacle appeared when {w2} complicated every step.",
                        f"But {w2} made even small choices feel big."
                    ]),
                    pick([
                        f"A twist arrived: the {helper} revealed a sign '{w3}'.",
                        f"Then everything flipped when they noticed '{w3}' glowing ahead."
                    ]),
                    pick([
                        f"The clue changed the shape of the afternoon.",
                        f"Suddenly, the path bent toward something kinder."
                    ]),
                    pick([
                        f"They followed the new way with steady breaths and bright eyes.",
                        f"They moved together, careful and {adj2}, step by step."
                    ]),
                    pick([
                        f"The solution felt simple once they stood side by side.",
                        f"In the end, the answer felt as light as a song."
                    ]),
                    pick([
                        f"They walked home carrying a quiet, happy lesson.",
                        f"They promised to remember how small twists can help."
                    ])
                ]
            else:
                lines = [
                    pick([
                        f"\"Did you bring {w1}?\" asked {pname} at the {place}.",
                        f"\"Is {w1} ready?\" {pname} wondered under the {adj1} light."
                    ]),
                    pick([
                        f"\"I did, but {w2} made everything tricky,\" said the {helper}.",
                        f"\"We tried, yet {w2} keeps tangling the plan,\" the {helper} sighed."
                    ]),
                    pick([
                        f"They paused beneath a board painted '{w3}', thinking things through.",
                        f"A wooden sign read '{w3}', and their eyes brightened."
                    ]),
                    pick([
                        f"\"Maybe we slow down and choose the kind path,\" {pname} realized.",
                        f"\"What if we go gently instead?\" {pname} said."
                    ]),
                    pick([
                        f"Together they tried again, softer this time.",
                        f"They teamed up and took one careful step."
                    ]),
                    pick([
                        f"It worked, and the feeling carried them into a calm ending.",
                        f"It clicked, and a hush of {feel} settled around them."
                    ]),
                    pick([
                        f"They promised to remember this little wisdom tomorrow.",
                        f"They smiled, ready to carry this moment forward."
                    ])
                ]
            # Middle segment expansion helpers to reach target length and reinforce theme and cause-effect
            def themed_tail(theme):
                tl = theme.strip().lower()
                if tl == 'funny':
                    return [
                        pick([f"A silly echo followed, and they laughed at the mix-up.", f"Someone snorted, and the {adj1} mood turned giggly."]),
                        pick([f"Because of that, even {w1} and {w2} felt like part of the joke.", f"So they decided {w1}, {w2}, and '{w3}' made a perfect punchline."]),
                        pick([f"They walked off grinning, trading little jokes about it all.", f"They ended the day with playful grins and light steps."])
                    ]
                elif tl == 'adventure':
                    return [
                        pick([f"They marked the map and promised a braver route tomorrow.", f"Footprints and starlight showed a farther road waiting."]),
                        pick([f"Because of the clue, {pname} felt the {feel} of the trail humming underfoot.", f"With the sign '{w3}', their hearts drummed softly, ready for the next path."]),
                        pick([f"So they packed {w1} carefully and moved on.", f"They kept {w2} safe this time and saluted the sign '{w3}'."])
                    ]
                elif tl == 'moral':
                    return [
                        pick([f"They chose honesty over hurry, and everything fit together.", f"Kindness steadied them when quick answers could not."]),
                        pick([f"Because they shared, the knot loosened.", f"They found that patience clears confusion like sunlight."]),
                        pick([f"The day closed with a simple lesson they agreed to keep.", f"They whispered the moral and tucked it gently into memory."])
                    ]
                elif tl == 'mystery':
                    return [
                        pick([f"A soft hush lingered, as if the {place} kept more clues.", f"Shadows stretched, hinting that another riddle might wait."]),
                        pick([f"Because the trail fit, {pname} traced '{w3}' with a finger and wondered what it hid.", f"They pocketed a tiny note about {w1} and {w2} for later."]),
                        pick([f"Answers came, but the last line of the puzzle stayed coy.", f"They left with {feel}, sensing part two was just ahead."])
                    ]
                else:
                    return [
                        pick([f"They spoke softly, hands close, letting the moment bloom.", f"A quiet warmth blossomed between them like a lantern."]),
                        pick([f"Because of that, {pname} noticed how {w1} and {w2} seemed to belong here.", f"Even '{w3}' felt like a promise in the evening air."]),
                        pick([f"They carried the feeling home, hearts light and sure.", f"They walked away smiling, grateful for this gentle turn."])
                    ]

            target_len = random.randint(12, 18)
            while len(lines) < max(10, target_len):
                lines.extend(themed_tail(theme))
                if len(lines) > 25:
                    break
            tl = theme.strip().lower()
            if tl == 'moral':
                if not any(ln.lower().startswith('the moral:') for ln in lines[-3:]):
                    lines.append(pick([
                        f"The moral: patience and kindness untie the hardest knots.",
                        f"The moral: honesty, shared gently, clears confusion.",
                        f"The moral: courage with care turns trouble into wisdom."
                    ]))
            elif tl == 'romantic':
                lines.append(pick([
                    f"Their hearts settled into a quiet, certain yes.",
                    f"They held the moment softly, knowing it was real.",
                    f"They chose each other, and the evening felt complete."
                ]))
            elif tl == 'adventure':
                lines.append(pick([
                    f"They discovered more than a path—they found steady courage.",
                    f"They grew a little braver, and the map seemed bigger.",
                    f"Discovery met them at the edge of the next turn."
                ]))
            elif tl == 'mystery':
                lines.append(pick([
                    f"A final clue clicked into place with a soft, satisfying hush.",
                    f"The reveal made sense at last, like a door opening quietly.",
                    f"What seemed hidden all along had simply waited to be seen."
                ]))
            elif tl == 'funny':
                lines.append(pick([
                    f"They laughed again, promising to label everything next time.",
                    f"They agreed the best plan was a checklist—and a snack.",
                    f"They waved goodbye, still chuckling about the whole mix-up."
                ]))
            if len(lines) > 25:
                lines = lines[:25]
            return "\n".join(lines)

        # Build prompt based on configured template
        prompt_template = os.getenv('PROMPT_TEMPLATE', '').strip().lower()
        use_mistral_template = prompt_template == 'mistral'
        if prompt_template in ('user', 'structured', 'all', 'adventure'):
            # User-requested storybook-style template for all themes
            keywords_str = ', '.join(user_words)
            prompt = (
                f"""
You are a story-writing AI. Write a complete, storybook-style story with a proper narrative: beginning, middle, and end.

Requirements:
1) Start the story EXACTLY with "Once upon a time," on the first line.
2) Theme: {theme}. The story must be 100% consistent with this theme.
3) Include all the following keywords naturally within the story: {keywords_str}. Use them logically in context.
4) Story length: 150–300 words.
5) Ensure the story is engaging, coherent, and logical. Characters, events, and places should make sense together.
6) Repetition is allowed only if it feels natural.
7) Use rich, storybook-style language that gives the feeling of reading a real story.
8) Avoid random statements or disconnected dialogues; make the narrative flow like a storybook.
9) End with a satisfying conclusion, moral, or resolution if appropriate.

Output only the story text (no extra commentary).
""".strip()
            )
        elif use_mistral_template:
            keywords = ', '.join(user_words)
            prompt = (
                f"""
You are a creative story-writing AI.
Write a story of at between 10 - 25  lines based on the following details:

Theme: {theme}
Keywords: {keywords}

The story must:
- Be completely related to the given theme.
- Include all given keywords naturally in the sentences.
- Have a clear beginning, middle, and ending.
- Be creative, emotional, and logical (no random jumps).
- Avoid repetition or irrelevant details.

Now, write the full story.
""".strip()
            )
        else:
            prompt = (
                f"""
                You are an advanced AI storyteller.
                Follow these steps exactly:
                1) Input: Keywords = {', '.join(user_words)}. Theme = {theme}.
                2) Understand: Identify meaning/context of each keyword and imagine a coherent scene connecting them.
                3) Theme adaptation: {theme_guidance}
                4) Structure: Use this structure -> {structure}
                5) Creativity: Do NOT reuse any fixed template; introduce fresh characters/settings/plot directions; {twist}. Use different character names and a distinct setting from any previous story in this session.
                6) Output rules: 150–300 words; start with a natural opening (e.g., "Once upon a time", "One day", or similar); natural inclusion of ALL keywords; clear logical flow; correct grammar. Must have Beginning (characters+setting), Middle (theme-related event/conflict/twist), and End (clear resolution). For Moral, explicitly include a final lesson line beginning with 'The moral:'; for Romantic, provide an emotional resolution; for Adventure, show discovery or growth; for Mystery, reveal a surprising but logical detail; for Funny, end with a witty or playful twist.
                Additional constraints: Write in {style}. Keep sentences clear; avoid bulleting. Content must be safe, positive, and appropriate for all ages.
                Important: Do not echo these instructions, only output the story text.
                Uniqueness nonce: {nonce}. Do not include or mention this nonce in the story text.
                """.strip()
            )

        token_present = bool(os.getenv('HF_API_TOKEN', '').strip())
        if pre_generated:
            generated = pre_generated
        else:
            if token_present:
                generated = call_hf_api(prompt)
                if isinstance(generated, str) and generated.startswith("A friendly hiccup in the magic cloud!"):
                    generated = local_generate_story(user_words, theme, structure)
            else:
                generated = local_generate_story(user_words, theme, structure)

        # Try to trim prompt echo if model returns prompt+continuation
        if generated.startswith(prompt):
            generated = generated[len(prompt):].strip()

        # Remove any accidental nonce leakage
        if 'Uniqueness nonce:' in generated:
            generated = '\n'.join([ln for ln in generated.splitlines() if 'Uniqueness nonce:' not in ln])

        # Light post-process: ensure ends with period
        if generated and not generated.strip().endswith(('.', '!', '?', '”', '"')):
            generated = generated.strip() + '.'

        # Ensure ALL user words appear (case-insensitive). If missing, retry once with stricter instruction, then append a natural line.
        if user_words:
            def missing_words(text: str):
                lt = text.lower()
                return [w for w in user_words if w.lower() not in lt]

            missing = missing_words(generated)
            if missing:
                strict_prompt = (
                    f"""
                    Revise the story to 150–300 words. Include EACH of these words exactly as written and used naturally: {', '.join(user_words)}.
                    Keep the same theme ({theme}), coherence, chosen structure ({structure}), and friendly tone. Ensure clear Beginning, Middle, End with cause-and-effect connectors (because, so, therefore), start with a natural opening, and use a theme-appropriate ending as specified.
                    """.strip()
                )
                regenerated = call_hf_api(strict_prompt)
                if regenerated and regenerated.startswith(strict_prompt):
                    regenerated = regenerated[len(strict_prompt):].strip()
                if regenerated:
                    generated = regenerated
                # Re-check; if still missing, append a natural closing line using the missing words
                missing = missing_words(generated)
                if missing:
                    add_line = "In the end, they remembered " + ", ".join(missing[:-1]) + (" and " + missing[-1] if len(missing) > 1 else missing[0]) + ", woven kindly into their day."
                    generated = generated.rstrip() + "\n" + add_line

        # Enforce 150–300 words and natural opening
        def count_words(text: str) -> int:
            import re
            return len(re.findall(r"\b\w+\b", text))

        def ensure_opening(text: str) -> str:
            body = text.strip()
            if not body:
                return "Once upon a time,"
            first = body.splitlines()[0]
            # Normalize leading quotes/backticks/spaces
            def norm(s: str) -> str:
                return s.lstrip(' \t\u201c\u201d\"\'\`')
            if not norm(first).lower().startswith("once upon a time,"):
                return "Once upon a time,\n" + body
            return body

        def ensure_closing(text: str) -> str:
            closing_lines = [ln.strip() for ln in text.strip().splitlines() if ln.strip()]
            last = closing_lines[-1] if closing_lines else ""
            # If the last line already feels conclusive, keep it
            conclusive_endings = (
                "ever after.",
                "the end.",
                "the end!",
                "the end?",
                "the moral:",
                "lesson:",
                "at last.",
                "at last!",
                "in the end.",
                "in the end!",
                "and so it was.",
            )
            if last.lower().endswith(conclusive_endings) or last.lower().startswith(("the moral:", "moral:")):
                return text
            # Theme-specific classic closures
            theme_closers = {
                'romantic': "And they carried this quiet joy forward, ever after.",
                'adventure': "And so the journey ended, leaving courage and wonder in their hearts.",
                'moral': "The moral: kindness and honesty guide every path to a gentle end.",
                'mystery': "At last, the final clue fit, and the truth rested quietly in place.",
                'funny': "And they laughed about it all the way home—what a day!",
            }
            closer = theme_closers.get(t, "And so the day closed softly, with everything in its right place.")
            return text.rstrip() + "\n" + closer

        if not use_mistral_template:
            generated = ensure_opening(generated)
            wc = count_words(generated)
            if wc < 150:
                if token_present:
                    expand_prompt = (
                        f"""
                        Expand the story to 180–240 words while keeping the same theme ({theme}), coherence, and natural inclusion of these words: {', '.join(user_words)}.
                        Maintain clear Beginning, Middle, End with cause-and-effect, and keep the existing tone and ending constraints.
                        Start with a natural opening and do not add lists or headers. Output plain text only.
                        """.strip()
                    )
                    expanded = call_hf_api(expand_prompt)
                    if expanded and expanded.startswith(expand_prompt):
                        expanded = expanded[len(expand_prompt):].strip()
                    if expanded:
                        generated = ensure_opening(expanded)
                # If still short after API attempt, do offline expansion as fallback
                wc = count_words(generated)
                if wc < 150:
                    # Offline expansion: extend with themed tails until target reached
                    add_chunks = []
                    while count_words(generated + ("\n" + "\n".join(add_chunks) if add_chunks else "")) < 170:
                        add_chunks.extend(themed_tail(theme))
                        if len(add_chunks) > 15:
                            break
                    if add_chunks:
                        generated = generated.rstrip() + "\n" + "\n".join(add_chunks)
            else:
                # Offline expansion: extend with themed tails until target reached
                add_chunks = []
                while count_words(generated + ("\n" + "\n".join(add_chunks) if add_chunks else "")) < 170:
                    add_chunks.extend(themed_tail(theme))
                    if len(add_chunks) > 15:
                        break
                if add_chunks:
                    generated = generated.rstrip() + "\n" + "\n".join(add_chunks)
            wc = count_words(generated)
            if wc > 300:
                # Trim by sentences to closest under 300 words
                import re
                sents = [s.strip() for s in re.split(r"(?<=[\.!?])\s+", generated) if s.strip()]
                out = []
                for s in sents:
                    if count_words(" ".join(out + [s])) <= 300:
                        out.append(s)
                    else:
                        break
                generated = " ".join(out)
            # Ensure a classic closing line
            generated = ensure_closing(generated)

        # Final guard: always enforce classic opening/closing for all templates
        generated = ensure_opening(generated)
        generated = ensure_closing(generated)

        def jaccard(a: str, b: str):
            sa = set([x for x in a.lower().split() if x])
            sb = set([x for x in b.lower().split() if x])
            if not sa or not sb:
                return 0.0
            inter = len(sa & sb)
            union = len(sa | sb)
            return inter / union

        recent = session.get('recent_stories', [])
        too_similar = any(jaccard(generated, s) >= 0.5 for s in recent)
        if too_similar:
            alt_structure_options = [
                "Beginning → Problem → Resolution",
                "Character Introduction → Conflict → Climax → Ending",
                "Event Start → Obstacle → Twist → Resolution",
                "Dialogue → Conflict → Realization → Ending",
            ]
            alt_structure = random.choice([s for s in alt_structure_options if s != structure] or alt_structure_options)
            regen_prompt = (
                f"""
                Generate a completely new story that is substantially different from previous outputs.
                Keywords: {', '.join(user_words)}. Theme: {theme}.
                Use structure: {alt_structure}. Do not reuse phrasing from typical responses.
                Length 150–300 words, include all keywords naturally, clear logical flow with cause-and-effect connectors, correct grammar.
                Start with a natural opening. End with the theme-specific resolution (Moral -> "The moral: ...", Romantic -> emotional connection, Adventure -> discovery/growth, Mystery -> clear reveal, Funny -> playful twist).
                Write in {style}. Output plain text only.
                """.strip()
            )
            regenerated = call_hf_api(regen_prompt)
            if regenerated and regenerated.startswith(regen_prompt):
                regenerated = regenerated[len(regen_prompt):].strip()
            if regenerated:
                def ensure_words(text: str):
                    lt = text.lower()
                    miss = [w for w in user_words if w.lower() not in lt]
                    if miss:
                        strict2 = (
                            f"""
                            Revise to 150–300 words. Include each word exactly as written and used naturally: {', '.join(user_words)}.
                            Keep theme {theme}. Ensure Beginning, Middle, End with cause-and-effect connectors, start with a natural opening, and end appropriately for the theme. Output plain text only.
                            """.strip()
                        )
                        r2 = call_hf_api(strict2)
                        if r2 and r2.startswith(strict2):
                            r2 = r2[len(strict2):].strip()
                        return r2 or text
                    return text
                regenerated = ensure_words(regenerated)
                ls = [ln.strip() for ln in regenerated.splitlines() if ln.strip()]
                if len(ls) < 6:
                    regenerated = generated
                elif len(ls) > 25:
                    regenerated = "\n".join(ls[:25])
                generated = regenerated

        recent.append(generated)
        if len(recent) > 5:
            recent = recent[-5:]
        session['recent_stories'] = recent
        session['last_style'] = style
        session['last_structure'] = structure

        return jsonify({'story': generated, 'theme': theme, 'words': words})

    @app.route('/save_story', methods=['POST'])
    @login_required
    def save_story():
        data = request.get_json(silent=True) or {}
        content = (data.get('content') or '').strip()
        theme = (data.get('theme') or '').strip()
        words = (data.get('words') or '').strip()
        if not content:
            return jsonify({'error': 'No story to save.'}), 400
        story = Story(user_id=current_user.id, theme=theme or 'Unknown', words=words or '', content=content)
        db.session.add(story)
        db.session.commit()
        return jsonify({'ok': True})

    @app.route('/my_stories')
    @login_required
    def my_stories():
        stories = Story.query.filter_by(user_id=current_user.id).order_by(Story.created_at.desc()).all()
        return render_template('my_stories.html', stories=stories)

    @app.route('/delete_story/<int:story_id>', methods=['POST'])
    @login_required
    def delete_story(story_id):
        story = Story.query.filter_by(id=story_id, user_id=current_user.id).first()
        if not story:
            return jsonify({'ok': False, 'error': 'Not found'}), 404
        db.session.delete(story)
        db.session.commit()
        return jsonify({'ok': True})

    return app


if __name__ == '__main__':
    app = create_app()
    # Determine port: prefer --port=XXXX CLI arg, else PORT env, else 5000
    import sys
    try:
        port = int(os.getenv('PORT', 5000))
    except Exception:
        port = 5000
    for arg in sys.argv[1:]:
        if arg.startswith('--port='):
            try:
                port = int(arg.split('=', 1)[1])
            except Exception:
                pass
    app.run(host='0.0.0.0', port=port, debug=True)
