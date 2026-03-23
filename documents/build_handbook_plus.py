#!/usr/bin/env python3
"""Build the 24-page FORGE Handbook Plus PDF using WeasyPrint."""

import base64

with open("/home/ubuntu/forge-site/images/forge-logo.png", "rb") as f:
    logo_b64 = base64.b64encode(f.read()).decode()

LOGO = f"data:image/png;base64,{logo_b64}"
MAROON = "#6B1C23"
BROWN = "#8B4513"
NAVY = "#1B4965"
GOLD = "#B8922E"

notes_lines = "".join(['<div class="nl">&nbsp;</div>' for _ in range(34)])

html = f"""<!DOCTYPE html>
<html><head><meta charset="utf-8">
<style>
@page {{
    size: 8.5in 11in;
    margin: 0.55in 0.65in 0.75in 0.65in;
    @top-left {{
        content: "FORGE";
        font-family: 'Liberation Sans', sans-serif;
        font-weight: bold; font-size: 8pt; color: {MAROON};
        padding-top: 0.1in;
    }}
    @bottom-center {{
        content: "Leadership begins when we stop living only for ourselves and start building others.";
        font-family: 'Liberation Sans', sans-serif;
        font-style: italic; font-size: 7pt; color: {MAROON};
    }}
    @bottom-right {{
        content: counter(page);
        font-family: 'Liberation Sans', sans-serif;
        font-size: 7pt; color: #888;
    }}
}}
@page:first {{
    @top-left {{ content: none; }}
    @bottom-center {{ content: none; }}
    @bottom-right {{ content: none; }}
}}
@page cover {{
    @top-left {{ content: none; }}
    @bottom-center {{ content: none; }}
    @bottom-right {{ content: none; }}
}}
@page backcover {{
    @top-left {{ content: none; }}
    @bottom-center {{ content: none; }}
    @bottom-right {{ content: none; }}
}}
@page tearout {{
    @top-left {{ content: none; }}
    @bottom-center {{ content: none; }}
    @bottom-right {{ content: none; }}
}}

body {{
    font-family: 'Liberation Sans', sans-serif;
    font-size: 9pt; line-height: 1.35; color: #222;
    text-align: justify; margin: 0; padding: 0;
}}
h1 {{
    font-size: 15pt; color: {MAROON}; margin: 0 0 8pt 0;
    text-align: left; line-height: 1.15;
}}
h2 {{
    font-size: 11.5pt; color: {BROWN}; margin: 8pt 0 4pt 0; line-height: 1.15;
}}
h3 {{
    font-size: 10pt; color: {NAVY}; margin: 6pt 0 3pt 0;
}}
p {{ margin: 3pt 0; }}
ul, ol {{ margin: 2pt 0; padding-left: 16pt; }}
li {{ margin-bottom: 1.5pt; }}
.pb {{ page-break-before: always; }}
.cover {{ page: cover; text-align: center; padding-top: 1in; }}
.cover img {{ width: 2.5in; display: block; margin: 0 auto 0.25in auto; }}
.cover .t {{ font-size: 30pt; color: {MAROON}; font-weight: bold; margin-bottom: 0.1in; }}
.cover .st {{ font-size: 12pt; font-style: italic; color: {BROWN}; margin-bottom: 0.5in; }}
.cover .m {{ font-size: 9.5pt; color: #333; text-align: justify; max-width: 5.5in; margin: 0 auto 0.4in auto; line-height: 1.45; }}
.cover .mt {{ font-size: 10.5pt; color: {MAROON}; font-style: italic; margin-top: 0.3in; }}
.backcover {{ page: backcover; text-align: center; padding-top: 2.2in; }}
.backcover img {{ width: 1.8in; display: block; margin: 0 auto 0.3in auto; }}
.tearout {{ page: tearout; }}
.db {{ border: 1.5px dashed #999; padding: 0.15in 0.2in; position: relative; }}
.sl {{ border-bottom: 1px solid #333; width: 3.2in; display: inline-block; margin-top: 0.25in; margin-right: 0.2in; }}
.slb {{ font-size: 7.5pt; color: #555; display: block; margin-top: 1pt; }}
.ds {{ border-bottom: 1px solid #333; width: 1.3in; display: inline-block; }}
.q {{ font-style: italic; color: {MAROON}; margin: 5pt 0; text-align: center; font-size: 9pt; }}
.qb {{ font-style: italic; color: {MAROON}; margin: 4pt 0.2in; text-align: center; font-size: 9.5pt; }}
.bx {{ border: 1.2px solid {NAVY}; border-radius: 3pt; padding: 5pt 8pt; margin: 5pt 0; background: #f7f9fb; }}
.bxg {{ border: 1.2px solid {GOLD}; border-radius: 3pt; padding: 5pt 8pt; margin: 5pt 0; background: #fdf8ef; }}
.c {{ text-align: center; }}
.b {{ font-weight: bold; }}
.sm {{ font-size: 8pt; }}
.smr {{ font-size: 7.5pt; color: #555; }}
.gt {{ font-weight: bold; color: {NAVY}; }}
.nl {{ border-bottom: 1px solid #ccc; height: 1.25em; margin: 0; }}
.ph {{ font-weight: bold; font-size: 9.5pt; margin: 5pt 0 1pt 0; }}
.mp {{ text-align: center; padding-top: 0.7in; }}
.mp .bh {{ font-size: 20pt; color: {MAROON}; font-weight: bold; margin-bottom: 0.35in; }}
.mp .qi {{ font-style: italic; color: {BROWN}; font-size: 10pt; margin: 0.18in 0.4in; line-height: 1.45; }}
.ct {{ font-size: 8.5pt; line-height: 1.4; }}
</style></head><body>

<!-- P1 COVER -->
<div class="cover">
<img src="{LOGO}" alt="FORGE">
<div class="t">FORGE Handbook</div>
<div class="st">Facilitating Opportunities for Reentry, Growth &amp; Empowerment</div>
<div class="m">FORGE's mission is to build mentors who lead by example, create conflict-free dorms, and live out the principle of Service Over Self &mdash; helping others grow, strengthening our communities, and turning time served into time that serves others.</div>
<div class="mt">"Leadership begins when we stop living only for ourselves<br>and start building others."</div>
</div>

<!-- P2 ELEVATOR SPEECH -->
<div class="pb">
<h1>Elevator Speech <span style="font-size:10pt;font-weight:normal;color:{BROWN};">(You need to memorize this.)</span></h1>
<h2>FORGE &mdash; Facilitating Opportunities for Reentry, Growth &amp; Empowerment</h2>
<p><strong>"We're building a new prison experience &mdash; where men lead by example, support one another, and prepare to make a positive impact &mdash; both inside these walls and beyond them."</strong></p>
<p>"Our goal is simple: to turn time served into time that serves others."</p>
<h2>Our Purpose</h2>
<p>To build mentors who create a culture of peace, responsibility, and service &mdash; modeling the change we want to see in every community.</p>
<p>When someone asks you what FORGE is, this is what you tell them. Not a rehearsed speech &mdash; but a real answer, from someone who lives it. You should be able to explain FORGE in 30 seconds or less, in your own words, with conviction.</p>
<p>If you can't explain what you're part of, you're not really part of it yet. Learn it. Own it. Live it.</p>
<p class="q">"If you can't explain it simply, you don't understand it well enough."</p>
<p>Practice with your mentor. Practice with your cellmate. Practice until it's second nature. Because one day, someone &mdash; maybe a counselor, maybe a parole board member, maybe your family &mdash; is going to ask you what FORGE is. And your answer will say everything about how seriously you've taken this journey.</p>
</div>

<!-- P3 STAKEHOLDER -->
<div class="pb">
<h1>You Are a Stakeholder</h1>
<p>In the last several years, violence inside Georgia's prisons has sky-rocketed. Not just murders, but stabbings and fights, many of which are never even reported. Things must change. We all want to go home one day. This includes staff and inmates alike.</p>
<p>Many of us have come to see that we must take on some of the responsibility to build our own rehabilitation system and create a safer environment to live in. That's what FORGE is about.</p>
<h2>What Is a Stakeholder?</h2>
<p>A <strong>stakeholder</strong> is someone who has something at stake &mdash; something to gain or lose based on the outcome. In here, the outcome of every day is shaped by the behavior of the men around you. You are a stakeholder because the conditions you live in are directly affected by the conduct of your peers.</p>
<p>FORGE channels peer influence constructively. Instead of letting negativity, chaos, and violence define the culture, FORGE trains men to reduce harm, resolve conflict before it escalates, and build others up rather than tear them down.</p>
<h2>What It Means</h2>
<p>Being a stakeholder means accepting that your actions affect not only yourself, but everyone living around you &mdash; including staff. It means choosing restraint over reaction, accountability over avoidance, and stability over chaos. You are part of the solution.</p>
<p>Every time you walk away from a confrontation, every time you check on someone who's struggling, every time you hold yourself to a higher standard &mdash; you are exercising your stake in this community.</p>
<p class="q">"The environment won't change until the men inside it decide to change it."</p>
</div>

<!-- P4 WHAT THAT LOOKS LIKE -->
<div class="pb">
<h1>What That Looks Like</h1>
<p>Being a stakeholder isn't a title &mdash; it's a practice. It shows up in the small decisions you make every day:</p>
<ul>
<li><strong>Step in early</strong> &mdash; recognize tension before it becomes violence and intervene with calm, trained skill</li>
<li><strong>Offer support</strong> &mdash; be the person someone can turn to before they make a destructive choice</li>
<li><strong>Own your mistakes</strong> &mdash; accountability isn't weakness; it's the foundation of trust</li>
<li><strong>Hold the line on standards</strong> &mdash; don't let the culture slide because it's easier to look the other way</li>
<li><strong>Model restraint</strong> &mdash; your composure under pressure teaches more than any lecture</li>
<li><strong>Invest in others</strong> &mdash; share what you've learned, mentor someone newer, be available</li>
</ul>
<p>This does <em>not</em> replace staff authority. FORGE complements the institutional structure by creating a layer of trained, peer-based support that makes everyone's job &mdash; and everyone's life &mdash; easier and safer.</p>
<p class="b">"A dorm where trained mentors are actively building peace is a dorm that is safer for everyone."</p>
<h2>The Ripple Effect</h2>
<p>When one man changes, his cell changes. His dorm changes. His family feels it. His community feels it. FORGE doesn't just change individuals &mdash; it changes environments. The work you do here reaches far beyond these walls.</p>
<p>Think about it: if you change, and you help one other person change, and he helps one more &mdash; the math starts to matter. That's how cultures shift. Not through mandates, but through influence. And you have more influence than you think.</p>
<div class="bx"><p class="c b" style="color:{MAROON};margin:0;">"You have more power to change this environment than you realize. FORGE gives you the skills to use that power responsibly."</p></div>
</div>

<!-- P5 CURRICULUM -->
<div class="pb">
<h1>The FORGE Curriculum</h1>
<p>FORGE is a <strong>36-week, 108-session training program</strong> designed to take participants from self-awareness through active mentoring leadership. The curriculum is rigorous, structured, and progressive &mdash; each phase builds on the one before it.</p>
<div class="bx">
<h3 style="margin-top:0;">Phase 1: Foundation &mdash; "Know Yourself" <span style="font-size:9pt;font-weight:normal;">(Weeks 1&ndash;12)</span></h3>
<p>The foundation of everything. You'll develop core CBT skills, learn to identify and interrupt thinking errors, build emotional regulation techniques, practice conflict resolution, and begin building a culture of personal accountability. This is where you learn to lead yourself before you can lead anyone else.</p>
</div>
<div class="bx">
<h3 style="margin-top:0;">Phase 2: Development &mdash; "Build Others" <span style="font-size:9pt;font-weight:normal;">(Weeks 13&ndash;24)</span></h3>
<p>Now you learn to teach. Phase 2 introduces adult learning principles, lesson planning, facilitation skills, motivational interviewing (OARS), simulation-based training, and restorative justice practices. You'll practice co-facilitation and learn the ethics and boundaries of mentoring.</p>
</div>
<div class="bx">
<h3 style="margin-top:0;">Phase 3: Practicum &mdash; "Lead and Serve" <span style="font-size:9pt;font-weight:normal;">(Weeks 25&ndash;36)</span></h3>
<p>This is where it all comes together. You'll complete supervised mentoring, co-facilitate Phase 1 sessions with new participants, conduct 1-on-1 mentoring, lead community circles, and accumulate 60+ field hours. The phase culminates in a review board certification.</p>
</div>
<h2>Gate Requirements</h2>
<ul>
<li>85% attendance in the current phase</li>
<li>Passing written assessments</li>
<li>Satisfactory peer evaluations</li>
<li>Positive staff observation reports</li>
<li>Completed portfolio items for the phase</li>
</ul>
</div>

<!-- P6 WHAT YOU'LL LEARN -->
<div class="pb">
<h1>What You'll Learn</h1>
<p class="ph" style="color:{NAVY};">Phase 1: Foundation Skills</p>
<ul>
<li>Identifying and interrupting <strong>thinking errors</strong> (cognitive distortions)</li>
<li>Understanding the <strong>escalation curve</strong> &mdash; how conflicts build and where to intervene</li>
<li><strong>4-4-4 breathing</strong> and <strong>5-4-3-2-1 grounding</strong> techniques</li>
<li>Using <strong>"I" statements</strong> to communicate without blame</li>
<li>The <strong>FORGE 5-Step Conflict Resolution</strong> model</li>
<li>The <strong>accountability spectrum</strong> &mdash; from denial to ownership</li>
<li>Building a <strong>growth mindset</strong> &mdash; effort over talent, progress over perfection</li>
</ul>
<p class="ph" style="color:{GOLD};">Phase 2: Development Skills</p>
<ul>
<li><strong>Adult learning principles</strong> &mdash; how adults learn differently and how to teach effectively</li>
<li><strong>Lesson planning</strong> and structured session delivery</li>
<li><strong>OARS</strong> motivational interviewing &mdash; Open questions, Affirmations, Reflections, Summaries</li>
<li><strong>Simulation scenarios</strong> &mdash; practicing responses to realistic situations</li>
<li><strong>Restorative circles</strong> and facilitated dialogue</li>
<li><strong>Co-facilitation</strong> techniques and dynamics</li>
<li><strong>Ethics and boundaries</strong> in mentoring relationships</li>
</ul>
<p class="ph" style="color:{MAROON};">Phase 3: Practicum Skills</p>
<ul>
<li>Co-facilitation of Phase 1 sessions with new cohorts</li>
<li>One-on-one mentoring with assigned mentees</li>
<li>Leading independent sessions and community circles</li>
<li>Conflict mediation in real-time situations</li>
<li>Self-care practices to prevent burnout</li>
<li>Review board certification preparation and presentation</li>
</ul>
<div class="bxg"><p style="margin:0;font-size:8.5pt;"><em>The curriculum is built from programs proven to work in prisons across the country &mdash; Thinking for a Change, Moral Reconation Therapy, GRIP, Seeking Safety, and others. FORGE adapts these evidence-based approaches into a unified mentor-training framework.</em></p></div>
</div>

<!-- P7 LEADERSHIP THROUGH SERVICE -->
<div class="pb">
<h1>Leadership Through Service</h1>
<p>In FORGE, leadership begins with service. Not rank. Not reputation. Not how long you've been down. Leadership is measured by one thing: <em>how you treat the people around you</em>.</p>
<h2 style="font-size:10pt;">1. Be the Example</h2>
<p>Don't tell people how to act &mdash; show them. Your daily conduct is the most powerful teaching tool you have. When you handle frustration with composure, when you keep your word, when you treat people with respect even when they don't earn it &mdash; you are leading.</p>
<h2 style="font-size:10pt;">2. Serve First</h2>
<p>Service Over Self is not a slogan. It's a way of life. Look for ways to make someone else's day better. Help the new guy figure out the system. Check on the quiet one.</p>
<h2 style="font-size:10pt;">3. Protect the Culture</h2>
<p>The culture in your dorm is either being built or being destroyed &mdash; there is no neutral. Every interaction either contributes to a culture of peace or a culture of chaos. Protect the peace actively.</p>
<h2 style="font-size:10pt;">4. Reject Weapons and Violence</h2>
<p>There are no exceptions. FORGE participants commit fully to non-violence. Carrying or concealing weapons, or using violence to solve problems, is incompatible with everything this program stands for.</p>
<h2 style="font-size:10pt;">5. Teach What You Know</h2>
<p>Knowledge that stays locked inside your head helps no one. When you learn something that works &mdash; a breathing technique, a way to reframe a thought, a de-escalation approach &mdash; pass it on.</p>
<h2 style="font-size:10pt;">6. Hold Yourself to a Higher Standard</h2>
<p>As a FORGE participant, you are held to a higher standard than the general population. Your behavior in the dorm, in the chow hall, on the yard &mdash; everywhere &mdash; reflects on the program. When you fall short, own it. When you succeed, share it.</p>
<p class="q">"Service Over Self isn't sacrifice &mdash; it's purpose."</p>
</div>

<!-- P8 ATTITUDE & MINDSET -->
<div class="pb">
<h1>Attitude &amp; Mindset: The Foundation of Reentry</h1>
<h2>The Power of Attitude</h2>
<p>Your attitude is the one thing no one can take from you. Not the system, not your circumstances, not the people around you. You get to choose how you respond to everything that happens to you. That choice is the most powerful tool you have.</p>
<p>A man with a bad case and a good attitude will always go further than a man with a good case and a bad attitude. If you can't manage your mindset in here, where everything is structured, how will you manage it out there?</p>
<h2>Building a Winning Mindset</h2>
<div class="bx" style="padding:4pt 7pt;">
<p><strong style="color:{NAVY};">1. Ownership Over Blame</strong> &mdash; Stop pointing fingers. Even if others played a role in your situation, <em>you</em> are the one who has to build your way out. Ownership is freedom.</p>
<p class="q" style="margin:2pt 0;">"You can't change what you won't take responsibility for."</p>
</div>
<div class="bx" style="padding:4pt 7pt;">
<p><strong style="color:{NAVY};">2. Growth Over Comfort</strong> &mdash; Growth is uncomfortable. It means admitting you were wrong, trying things that feel awkward, failing and trying again. But the alternative &mdash; staying the same &mdash; leads right back to where you started.</p>
<p class="q" style="margin:2pt 0;">"If it doesn't challenge you, it doesn't change you."</p>
</div>
<div class="bx" style="padding:4pt 7pt;">
<p><strong style="color:{NAVY};">3. Purpose Over Impulse</strong> &mdash; Every decision either moves you toward your goals or away from them. Train yourself to pause. Ask: <em>"Does this serve my purpose?"</em> If not, don't do it.</p>
<p class="q" style="margin:2pt 0;">"Discipline is choosing between what you want now and what you want most."</p>
</div>
<div class="bx" style="padding:4pt 7pt;">
<p><strong style="color:{NAVY};">4. Service Over Self</strong> &mdash; The fastest way to find meaning is to help someone else. When you stop living only for yourself and start investing in others, everything changes &mdash; your perspective, your reputation, your sense of worth.</p>
<p class="q" style="margin:2pt 0;">"Your attitude, not your aptitude, will determine your altitude."</p>
</div>
</div>

<!-- P9 CONFLICT RESOLUTION -->
<div class="pb">
<h1>Conflict Resolution</h1>
<p><strong>Goal:</strong> Resolve disagreements before they escalate. Not every conflict needs a fight. Most don't even need a raised voice. The goal is to protect the peace.</p>
<h2>The FORGE 5-Step Model</h2>
<div class="bx">
<p><strong style="color:{NAVY};">Step 1: STOP</strong> &mdash; Pause before reacting. Take a breath. Create space between the trigger and your response.</p>
<p><strong style="color:{NAVY};">Step 2: THINK</strong> &mdash; What's really happening here? What am I feeling? What's at stake?</p>
<p><strong style="color:{NAVY};">Step 3: LISTEN</strong> &mdash; Let the other person speak. Don't interrupt. Just listen.</p>
<p><strong style="color:{NAVY};">Step 4: SPEAK</strong> &mdash; Use "I" statements. Express your perspective without accusations.</p>
<p><strong style="color:{NAVY};">Step 5: RESOLVE</strong> &mdash; Find common ground. What can both of you live with? What does peace look like?</p>
</div>
<h2>Red Lines</h2>
<p>Some situations are beyond peer resolution. If any of these are present, <strong>step back and notify staff immediately</strong>:</p>
<ul>
<li>Weapons are present or threatened</li>
<li>Someone is in immediate physical danger</li>
<li>Sexual assault or abuse is involved</li>
<li>A person is in a mental health crisis</li>
<li>Gang directives are driving the conflict</li>
</ul>
<h2>Quick Scripts</h2>
<p><em>"Hey, I can see this is getting heated. Let's take a step back."</em></p>
<p><em>"I hear you. I'm not trying to disrespect you. Let's figure this out."</em></p>
<p><em>"We don't have to agree &mdash; we just have to keep it peaceful."</em></p>
<p><em>"Let's both cool off and come back to this in 20 minutes."</em></p>
<p class="q">"The goal isn't to win the argument &mdash; it's to protect the peace."</p>
</div>

<!-- P10 DORM STANDARDS -->
<div class="pb">
<h1>Dorm Standards &amp; Rules</h1>
<h2 style="font-size:10pt;">Respect</h2>
<p>Treat every person &mdash; inmates and staff alike &mdash; with basic human respect. No slurs, no threats, no intimidation. Disrespect erodes trust and trust is the foundation of everything we're building.</p>
<h2 style="font-size:10pt;">Clean &amp; Quiet</h2>
<p>Keep your area clean. Keep common areas clean. Respect quiet hours. A clean, orderly environment reflects a disciplined mindset.</p>
<h2 style="font-size:10pt;">Property</h2>
<p>Don't touch what isn't yours. Borrowing without asking is stealing. Gambling creates debts, and debts create violence. Neither has a place in a FORGE dorm.</p>
<h2 style="font-size:10pt;">Weapons &amp; Safety</h2>
<p>Zero tolerance. No weapons. No exceptions. If you see one, report it. This isn't snitching &mdash; it's protecting the community you've committed to building.</p>
<h2 style="font-size:10pt;">Communication Standards</h2>
<p>Address staff respectfully &mdash; "yes sir," "no ma'am" is the baseline, not the ceiling. Handle disagreements with peers through conversation, not confrontation. When a situation exceeds your ability, escalate to a mentor or facilitator.</p>
<h2 style="font-size:10pt;">Mediation First</h2>
<p>Before any conflict escalates beyond words, seek mediation. Find a trained FORGE mentor. Use the 5-step model. Give peace a chance to work before positions harden. Most conflicts that turn violent could have been resolved with a 10-minute conversation.</p>
<h2 style="font-size:10pt;">Class &amp; Program Requirements</h2>
<p>Attend every session. Be on time. Come prepared. Participation isn't optional &mdash; it's the commitment you made when you joined this program. If you have a scheduling conflict, communicate it in advance. Three unexcused absences trigger a program review.</p>
<p class="q">"Standards aren't restrictions &mdash; they're the scaffolding for the culture we're building."</p>
</div>

<!-- P11 TEAR-OUT: FACILITATOR'S COPY -->
<div class="pb tearout">
<div style="border-left:2px dashed #999; padding-left:8pt; margin-left:-0.3in; font-size:7pt; color:#999; margin-bottom:4pt;">&#9986; TEAR ALONG FOLD</div>
<div class="db">
<h1 style="text-align:center;font-size:14pt;">Participant Commitment &amp; Signature</h1>
<p class="c b" style="color:{GOLD};font-size:11pt;">FACILITATOR'S COPY</p>
<div class="ct">
<p>By signing below, I commit to the following:</p>
<ul>
<li>I will uphold the FORGE Code of Conduct at all times.</li>
<li>I will attend all scheduled sessions and arrive on time.</li>
<li>I will treat all participants, facilitators, and staff with respect.</li>
<li>I will reject violence and weapons in all forms.</li>
<li>I will hold myself accountable and accept feedback.</li>
<li>I will practice Service Over Self in my daily actions.</li>
<li>I will protect the culture of peace in my dorm and community.</li>
<li>I will mentor and support others to the best of my ability.</li>
<li>I understand that violation of these commitments may result in removal from the program.</li>
</ul>
<p>I enter FORGE voluntarily, with the understanding that this program demands effort, accountability, and growth. I am ready.</p>
<p style="margin-top:0.3in;"><span class="sl"></span><br><span class="slb">Participant Printed Name</span></p>
<p><span class="sl"></span> &nbsp; <span class="ds"></span><br><span class="slb">Participant Signature &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; Date</span></p>
<p style="margin-top:0.2in;"><span class="sl"></span><br><span class="slb">Mentor / Witness Printed Name</span></p>
<p><span class="sl"></span> &nbsp; <span class="ds"></span><br><span class="slb">Mentor / Witness Signature &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; Date</span></p>
</div>
<p class="smr c" style="margin-top:0.15in;">This page may be removed from the handbook and submitted to your FORGE facilitator.</p>
</div>
</div>

<!-- P12 TEAR-OUT: BACK FACILITATOR -->
<div class="pb tearout">
<div class="mp">
<div class="bh">Service Over Self</div>
<div class="qi">"Leadership begins when we stop living only for ourselves<br>and start building others."</div>
<div class="qi">"Real leaders don't rise above others &mdash;<br>they lift others with them."</div>
<div class="qi">"The goal isn't to win the argument &mdash;<br>it's to protect the peace."</div>
<div class="qi">"Your attitude, not your aptitude,<br>will determine your altitude."</div>
<div class="qi">"What you rehearse in here<br>becomes who you are out there."</div>
<div class="qi" style="margin-top:0.3in;color:{MAROON};font-size:11pt;">"FORGE is more than a name &mdash; it's a process."</div>
</div>
</div>

<!-- P13 TEAR-OUT: PARTICIPANT'S COPY -->
<div class="pb tearout">
<div style="border-left:2px dashed #999; padding-left:8pt; margin-left:-0.3in; font-size:7pt; color:#999; margin-bottom:4pt;">&#9986; TEAR ALONG FOLD</div>
<div class="db">
<h1 style="text-align:center;font-size:14pt;">Participant Commitment &amp; Signature</h1>
<p class="c b" style="color:{NAVY};font-size:11pt;">YOUR COPY</p>
<div class="ct">
<p>By signing below, I commit to the following:</p>
<ul>
<li>I will uphold the FORGE Code of Conduct at all times.</li>
<li>I will attend all scheduled sessions and arrive on time.</li>
<li>I will treat all participants, facilitators, and staff with respect.</li>
<li>I will reject violence and weapons in all forms.</li>
<li>I will hold myself accountable and accept feedback.</li>
<li>I will practice Service Over Self in my daily actions.</li>
<li>I will protect the culture of peace in my dorm and community.</li>
<li>I will mentor and support others to the best of my ability.</li>
<li>I understand that violation of these commitments may result in removal from the program.</li>
</ul>
<p>I enter FORGE voluntarily, with the understanding that this program demands effort, accountability, and growth. I am ready.</p>
<p style="margin-top:0.3in;"><span class="sl"></span><br><span class="slb">Participant Printed Name</span></p>
<p><span class="sl"></span> &nbsp; <span class="ds"></span><br><span class="slb">Participant Signature &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; Date</span></p>
<p style="margin-top:0.2in;"><span class="sl"></span><br><span class="slb">Mentor / Witness Printed Name</span></p>
<p><span class="sl"></span> &nbsp; <span class="ds"></span><br><span class="slb">Mentor / Witness Signature &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; Date</span></p>
</div>
<p class="smr c" style="margin-top:0.15in;">Keep this copy in your handbook as a reminder of your commitment.</p>
</div>
</div>

<!-- P14 TEAR-OUT: BACK PARTICIPANT -->
<div class="pb tearout">
<div class="mp">
<div class="bh">Service Over Self</div>
<div class="qi">"Leadership begins when we stop living only for ourselves<br>and start building others."</div>
<div class="qi">"You can't change what you won't take responsibility for."</div>
<div class="qi">"If it doesn't challenge you, it doesn't change you."</div>
<div class="qi">"Discipline is choosing between what you want now<br>and what you want most."</div>
<div class="qi">"The environment won't change until<br>the men inside it decide to change it."</div>
<h2 style="text-align:center;margin-top:0.35in;color:{MAROON};">My Personal Commitment</h2>
<div style="max-width:5in;margin:0 auto;">
<div class="nl">&nbsp;</div><div class="nl">&nbsp;</div><div class="nl">&nbsp;</div><div class="nl">&nbsp;</div><div class="nl">&nbsp;</div><div class="nl">&nbsp;</div><div class="nl">&nbsp;</div>
</div>
</div>
</div>

<!-- P15 ASSESSMENT -->
<div class="pb">
<h1>How You'll Be Evaluated</h1>
<p>FORGE uses a competency-based assessment system. You'll be evaluated in <strong>six core areas</strong>, scored on a 1&ndash;4 scale. Proficient (3) or higher is required in all areas to advance.</p>
<h2>The Six Competencies</h2>
<div class="bx" style="padding:3pt 7pt;"><p style="margin:1pt 0;"><strong style="color:{NAVY};">1. Self-Awareness</strong> &mdash; Can you identify your triggers, thinking errors, and emotional patterns? Do you demonstrate insight into how your behavior affects others?</p></div>
<div class="bx" style="padding:3pt 7pt;"><p style="margin:1pt 0;"><strong style="color:{NAVY};">2. Emotional Regulation</strong> &mdash; Can you manage your emotions under stress? Do you use breathing, grounding, and pausing consistently?</p></div>
<div class="bx" style="padding:3pt 7pt;"><p style="margin:1pt 0;"><strong style="color:{NAVY};">3. Conflict Resolution</strong> &mdash; Can you de-escalate situations effectively? Do you apply the 5-step model? Do you know when to step back?</p></div>
<div class="bx" style="padding:3pt 7pt;"><p style="margin:1pt 0;"><strong style="color:{NAVY};">4. Communication</strong> &mdash; Can you express yourself clearly using "I" statements? Do you listen actively? Can you give and receive feedback?</p></div>
<div class="bx" style="padding:3pt 7pt;"><p style="margin:1pt 0;"><strong style="color:{NAVY};">5. Accountability</strong> &mdash; Do you own your mistakes? Do you follow through on commitments? Do you accept consequences without deflection?</p></div>
<div class="bx" style="padding:3pt 7pt;"><p style="margin:1pt 0;"><strong style="color:{NAVY};">6. Mentoring Readiness</strong> &mdash; Can you teach what you've learned? Do you show patience, empathy, and appropriate boundaries?</p></div>
<h2>Scoring Scale</h2>
<p><strong>1 = Emerging</strong> &mdash; Awareness is growing but skills are not yet consistent.<br>
<strong>2 = Developing</strong> &mdash; Skills are present but need reinforcement.<br>
<strong>3 = Proficient</strong> &mdash; Consistently demonstrates the competency across settings.<br>
<strong>4 = Exemplary</strong> &mdash; Models the competency and helps others develop it.</p>
<h2 style="font-size:10pt;">Evaluation Methods</h2>
<p style="font-size:8.5pt;">Written assessments &bull; Simulation scoring &bull; Peer review &bull; Staff observation &bull; Portfolio review &bull; Review board presentation</p>
</div>

<!-- P16 CODE OF CONDUCT 1-3 -->
<div class="pb">
<h1>FORGE Code of Conduct</h1>
<h2 style="font-size:10.5pt;">1. Integrity &amp; Accountability</h2>
<ul>
<li>Be honest in all interactions &mdash; with staff, peers, and yourself.</li>
<li>Take ownership of your actions. No excuses, no deflection.</li>
<li>If you make a mistake, admit it, make it right, and learn from it.</li>
<li>Keep your word. If you say you'll do something, do it.</li>
<li>Accept consequences without retaliation or complaint.</li>
</ul>
<p class="q">"Integrity is what you do when no one is watching."</p>
<h2 style="font-size:10.5pt;">2. Leadership &amp; Service</h2>
<ul>
<li>Lead by example in every setting &mdash; dorm, yard, chow hall, classroom.</li>
<li>Put service before self-interest. Look for ways to help others.</li>
<li>Use your influence to build people up, never to tear them down.</li>
<li>Mentor with patience, humility, and respect for boundaries.</li>
<li>Protect the culture &mdash; don't be a bystander when standards slip.</li>
</ul>
<p class="q">"Real leaders don't rise above others &mdash; they lift others with them."</p>
<h2 style="font-size:10.5pt;">3. Learning &amp; Growth</h2>
<ul>
<li>Attend all sessions prepared and on time.</li>
<li>Engage actively &mdash; participate in discussions, exercises, and reflections.</li>
<li>Be open to feedback, even when it's uncomfortable.</li>
<li>Complete all assignments and portfolio requirements.</li>
<li>Embrace the struggle &mdash; growth requires discomfort.</li>
<li>Share what you learn with others.</li>
</ul>
<p class="q">"The mind, once stretched by a new idea, never returns to its original dimensions."</p>
</div>

<!-- P17 CODE OF CONDUCT 4-6 -->
<div class="pb">
<h1 style="font-size:14pt;">FORGE Code of Conduct <span style="font-size:11pt;font-weight:normal;">(continued)</span></h1>
<h2 style="font-size:10.5pt;">4. Peace &amp; Safety</h2>
<ul>
<li>Reject violence in all its forms &mdash; physical, verbal, and psychological.</li>
<li>Never carry, conceal, or tolerate weapons.</li>
<li>De-escalate conflicts using trained techniques.</li>
<li>Report genuine safety threats &mdash; this protects the community.</li>
<li>Refuse to participate in gambling, extortion, or intimidation.</li>
<li>Maintain awareness and intervene early when tensions rise.</li>
</ul>
<p class="q">"Peace is not the absence of conflict &mdash; it's the presence of trained people who know how to resolve it."</p>
<h2 style="font-size:10.5pt;">5. Community &amp; Conduct</h2>
<ul>
<li>Respect all people regardless of race, background, charges, or status.</li>
<li>Keep your living area and common spaces clean and orderly.</li>
<li>Follow institutional rules &mdash; FORGE operates within the system, not outside it.</li>
<li>Address staff with respect at all times.</li>
<li>Represent FORGE positively in every interaction.</li>
<li>Avoid gossip, manipulation, and divisive behavior.</li>
</ul>
<p class="q">"Your character is defined by how you treat people who can do nothing for you."</p>
<h2 style="font-size:10.5pt;">6. Mindset &amp; Mission</h2>
<ul>
<li>Choose purpose over impulse, every day.</li>
<li>Focus on what you can control &mdash; your attitude, your effort, your choices.</li>
<li>See setbacks as opportunities for growth, not reasons to quit.</li>
<li>Remember your "why" &mdash; the people counting on you, the life you're building.</li>
<li>Commit to being better today than you were yesterday.</li>
<li>Carry the FORGE mission beyond the program &mdash; into your dorm, your family, your future.</li>
</ul>
<p class="q">"What you rehearse in here becomes who you are out there."</p>
</div>

<!-- P18 MENTOR PIPELINE -->
<div class="pb">
<h1>The Mentor Pipeline &amp; What Comes After</h1>
<h2>The Self-Sustaining Mentor Pipeline</h2>
<p>FORGE is designed to be self-sustaining. Every graduate becomes a potential trainer for the next cohort. The most credible messengers in this environment aren't people who read about prison in a textbook. They're people who live it, who've done the work, and who can look someone in the eye and say, "I've been where you are."</p>
<p>The pipeline works like this: Phase 3 participants co-facilitate Phase 1 sessions. Certified mentors lead Phase 1 independently. Senior mentors oversee the process and train new facilitators. Each generation trains the next.</p>
<h2>What Certification Means</h2>
<p>You're not just completing a program &mdash; you're earning a credential. FORGE certification represents:</p>
<ul>
<li><strong>216 hours</strong> of structured training across three phases</li>
<li><strong>60+ field hours</strong> of supervised mentoring and facilitation</li>
<li>Panel evaluation by facilitators, staff, and certified mentors</li>
<li>Demonstrated proficiency in all six core competencies</li>
<li>A completed portfolio documenting your growth and work</li>
</ul>
<h2>After Certification</h2>
<ul>
<li><strong>6-month service commitment</strong> to actively mentor and support the next cohort</li>
<li>Opportunity to <strong>co-facilitate</strong> Phase 1 and Phase 2 sessions</li>
<li>Path to become a <strong>Senior Mentor</strong> with expanded responsibilities</li>
<li>Potential to <strong>train at other facilities</strong> as the program expands</li>
</ul>
<h2>Your Legacy</h2>
<p>The men you train will train others. Your impact continues long after you've moved on &mdash; to another facility, to reentry, to freedom. Every person you invest in carries a piece of what you taught them. That's a legacy no sentence can take away.</p>
<p class="q">"The true measure of a mentor is not how many people follow him &mdash; but how many go on to lead."</p>
</div>

<!-- P19 DE-ESCALATION QUICK REFERENCE -->
<div class="pb">
<h1>De-escalation Quick Reference</h1>
<div class="bx" style="background:#f0f4f8;">
<h3 style="margin-top:0;text-align:center;">The FORGE 5-Step Model</h3>
<table style="width:100%;font-size:8.5pt;border-collapse:collapse;">
<tr><td style="padding:2pt 6pt;font-weight:bold;color:{NAVY};width:60pt;">1. STOP</td><td style="padding:2pt 6pt;">Pause. Breathe. Do not react on impulse.</td></tr>
<tr><td style="padding:2pt 6pt;font-weight:bold;color:{NAVY};">2. THINK</td><td style="padding:2pt 6pt;">What's really happening? What am I feeling? What's at stake?</td></tr>
<tr><td style="padding:2pt 6pt;font-weight:bold;color:{NAVY};">3. LISTEN</td><td style="padding:2pt 6pt;">Let them speak. Don't interrupt. Hear what's underneath.</td></tr>
<tr><td style="padding:2pt 6pt;font-weight:bold;color:{NAVY};">4. SPEAK</td><td style="padding:2pt 6pt;">Use "I" statements. Stay calm. Acknowledge their perspective.</td></tr>
<tr><td style="padding:2pt 6pt;font-weight:bold;color:{NAVY};">5. RESOLVE</td><td style="padding:2pt 6pt;">Find common ground. What does peace look like here?</td></tr>
</table>
</div>
<h2 style="font-size:10pt;">"Read the Room" Checklist</h2>
<ul>
<li><strong>Body language:</strong> Clenched fists? Pacing? Squared-up posture? Invading space?</li>
<li><strong>Tone:</strong> Rising volume? Clipped words? Sarcasm masking anger?</li>
<li><strong>Positioning:</strong> Is someone cornered? Are people gathering? Exit blocked?</li>
<li><strong>History:</strong> Is there a prior beef? Has this been building?</li>
</ul>
<h2 style="font-size:10pt;">"What to Say" Scripts</h2>
<div class="bxg" style="font-size:8.5pt;">
<p style="margin:1pt 0;"><em>"Hey, let's take a walk. Tell me what's going on."</em></p>
<p style="margin:1pt 0;"><em>"I'm not here to judge &mdash; I just want to make sure everyone's good."</em></p>
<p style="margin:1pt 0;"><em>"I hear you, man. I get it. But let's handle this the right way."</em></p>
<p style="margin:1pt 0;"><em>"Is this worth what it could cost you?"</em></p>
<p style="margin:1pt 0;"><em>"Let's step away for a minute. We can come back to this."</em></p>
<p style="margin:1pt 0;"><em>"What would you tell your son to do right now?"</em></p>
</div>
<h2 style="font-size:10pt;">"When to Step Back"</h2>
<p>Know your limits. You are <strong>not</strong> security. Disengage and notify staff if:</p>
<ul>
<li>Weapons are visible or suspected</li>
<li>The person is beyond verbal reach</li>
<li>You feel physically unsafe</li>
<li>Multiple aggressors are involved</li>
</ul>
<h2 style="font-size:10pt;">Heat Scale Reference</h2>
<p><strong>1&ndash;3:</strong> Calm to mildly annoyed. Normal conversation works. <strong>4&ndash;6:</strong> Frustrated to angry. Active de-escalation needed. <strong>7&ndash;8:</strong> Highly agitated. Limit words, give space, stay calm. <strong>9&ndash;10:</strong> Crisis. Step back. Get staff. Safety first.</p>
</div>

<!-- P20 KEY TERMS -->
<div class="pb">
<h1>Key FORGE Terms &amp; Definitions</h1>
<p><span class="gt">Service Over Self</span> &mdash; The foundational FORGE principle: putting the needs of the community and others before personal comfort or self-interest.</p>
<p><span class="gt">Stakeholder</span> &mdash; Anyone with something at stake in the outcome. Every participant is a stakeholder in the safety and culture of their environment.</p>
<p><span class="gt">Parallel Process</span> &mdash; The phenomenon where the dynamics of one relationship mirror another. How a mentor treats a mentee often mirrors how the mentor was trained.</p>
<p><span class="gt">Normative Culture</span> &mdash; A community environment where positive behavior is the expected standard, maintained through peer accountability rather than authority alone.</p>
<p><span class="gt">Think-Feel-Act Cycle</span> &mdash; The CBT framework: thoughts drive feelings, feelings drive actions. Change the thought, change the outcome.</p>
<p><span class="gt">Thinking Error</span> &mdash; A cognitive distortion leading to faulty conclusions. Examples: all-or-nothing thinking, blaming, minimizing, victim stance.</p>
<p><span class="gt">Escalation Curve</span> &mdash; The predictable pattern of how conflicts intensify. Early intervention is more effective than late intervention.</p>
<p><span class="gt">STOP Technique</span> &mdash; Stop, Take a breath, Observe what you're feeling, Proceed with intention.</p>
<p><span class="gt">"I" Statement</span> &mdash; "I feel [emotion] when [behavior] because [impact]." Expresses perspective without blame.</p>
<p><span class="gt">SBI Feedback Model</span> &mdash; Situation, Behavior, Impact. A structured way to give constructive feedback without personal attacks.</p>
<p><span class="gt">Heat Scale</span> &mdash; A 1&ndash;10 self-assessment of emotional intensity. Helps identify when to use de-escalation tools.</p>
<p><span class="gt">Restorative Circle</span> &mdash; A facilitated group process for addressing harm, repairing relationships, and rebuilding trust.</p>
<p><span class="gt">OARS</span> &mdash; Open questions, Affirmations, Reflections, Summaries. Core motivational interviewing techniques.</p>
<p><span class="gt">Credible Messenger</span> &mdash; A person whose life experience gives them unique authority and trust with the population they serve.</p>
<p><span class="gt">Gate Requirements</span> &mdash; Benchmarks (attendance, assessments, evaluations) that must be met to advance between FORGE phases.</p>
</div>

<!-- P21 HELPFUL REMINDERS -->
<div class="pb">
<h1>Helpful Reminders &amp; Daily Practices</h1>
<h2 style="font-size:10pt;">Morning Check-in</h2>
<p>Start each day with these questions:</p>
<div class="bx" style="padding:3pt 7pt;">
<ul>
<li>Where am I on the heat scale right now? (1&ndash;10)</li>
<li>What's one thing I can do today to serve someone else?</li>
<li>Is there any unresolved conflict I need to address?</li>
<li>What's my intention for today?</li>
<li>Who might need a check-in from me?</li>
</ul>
</div>
<h2 style="font-size:10pt;">The 4 Integrity Tests</h2>
<div class="bxg" style="padding:3pt 7pt;">
<p><strong style="color:{NAVY};">The Mirror Test</strong> &mdash; Can I look at myself and respect what I see?</p>
<p><strong style="color:{NAVY};">The Mentor Test</strong> &mdash; Would I be comfortable if my mentor saw me doing this?</p>
<p><strong style="color:{NAVY};">The Front Page Test</strong> &mdash; Would I be okay if this showed up on the front page?</p>
<p><strong style="color:{NAVY};">The Child Test</strong> &mdash; Would I want my child to do what I'm about to do?</p>
</div>
<h2 style="font-size:10pt;">When You're Struggling</h2>
<ol>
<li><strong>Breathe</strong> &mdash; 4-4-4 breathing. Four seconds in, four hold, four out.</li>
<li><strong>Ground yourself</strong> &mdash; 5-4-3-2-1: five things you see, four you hear, three you touch, two you smell, one you taste.</li>
<li><strong>Find your mentor</strong> &mdash; That's what they're there for. No one does this alone.</li>
<li><strong>Use your tools</strong> &mdash; Every skill you've learned is a tool. Open the toolbox.</li>
<li><strong>Remember your why</strong> &mdash; Who are you doing this for? What's waiting for you?</li>
</ol>
<h2 style="font-size:10pt;">The 10-10-10 Rule</h2>
<div class="bx" style="padding:3pt 7pt;">
<p style="margin:0;">Before reacting, ask yourself:</p>
<p style="margin:2pt 0;"><strong style="color:{MAROON};">How will I feel about this in 10 minutes?</strong></p>
<p style="margin:2pt 0;"><strong style="color:{MAROON};">How will I feel about this in 10 months?</strong></p>
<p style="margin:2pt 0;"><strong style="color:{MAROON};">How will I feel about this in 10 years?</strong></p>
<p style="margin:0;">Most things that feel urgent now won't matter in 10 months. The decisions that will matter in 10 years deserve careful thought, not a snap reaction.</p>
</div>
</div>

<!-- P22 NOTES -->
<div class="pb">
<h1>Notes</h1>
{notes_lines}
</div>

<!-- P23 THE FORGE WAY -->
<div class="pb">
<div style="padding-top:1.3in;text-align:center;">
<h1 style="font-size:22pt;text-align:center;margin-bottom:0.4in;">The FORGE Way</h1>
<p style="font-size:11.5pt;color:#333;max-width:5in;margin:0 auto 0.25in auto;line-height:1.6;text-align:center;">
FORGE is more than a name &mdash; it's a process.<br>
Just as metal is refined by fire, character is shaped by struggle,<br>
and purpose is strengthened by service.
</p>
<p style="font-size:11.5pt;color:#333;max-width:5in;margin:0 auto 0.25in auto;line-height:1.6;text-align:center;">
Every act of patience, every moment of restraint,<br>
and every choice to help someone else<br>
builds who you are becoming.
</p>
<p style="font-size:11.5pt;color:#333;max-width:5in;margin:0 auto 0.4in auto;line-height:1.6;text-align:center;">
Leadership is not granted &mdash; it's forged.<br>
And in that process, we discover that<br>
service isn't sacrifice &mdash; it's freedom.
</p>
<p style="font-size:14pt;color:{MAROON};font-style:italic;font-weight:bold;max-width:5.5in;margin:0.4in auto;line-height:1.4;">
"Leadership begins when we stop living only for ourselves<br>and start building others."
</p>
</div>
</div>

<!-- P24 BACK COVER -->
<div class="pb backcover">
<div style="padding-top:2.2in;text-align:center;">
<img src="{LOGO}" alt="FORGE" style="width:1.8in;display:block;margin:0 auto 0.3in auto;">
<p style="font-size:13pt;color:{MAROON};font-weight:bold;margin-bottom:0.1in;">FORGE</p>
<p style="font-size:10.5pt;color:{BROWN};font-style:italic;margin-bottom:0.4in;">Facilitating Opportunities for Reentry, Growth &amp; Empowerment</p>
<p style="font-size:9.5pt;color:#444;margin-bottom:0.08in;">Dooly State Prison &mdash; Unadilla, Georgia</p>
<p style="font-size:8.5pt;color:#666;margin-bottom:0.25in;">A program of the Positive Outreach Development Society, Inc.</p>
<p style="font-size:7.5pt;color:#888;">Copyright 2026. All rights reserved.</p>
</div>
</div>

</body></html>
"""

with open("/home/ubuntu/forge-site/documents/FORGE_Handbook_Plus.html", "w") as f:
    f.write(html)
print(f"HTML written ({len(html)} chars)")
