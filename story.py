# story.py
# Dictionary-based scene system for the main game.
# Fill in images/paths with your assets.

story = {
    "start": {
        "text": "Your name is {name}. You lived in Kakako town most of your life alongside your mother. Your father left when you were 3. You were close with your neighbor Kaile — your best friend. One night at 10 PM you wander into the forest and see a familiar figure, it was Kaile.",
        "image": "forest1.png",
        "character": "player.png",
        "choices": [
            {"text": "Greet Kaile warmly", "next_scene": "talk", "affection": +6, "courage": +3},
            {"text": "Avoid Kaile silently", "next_scene": "avoid", "affection": -4, "courage": -2}
        ]
    },

    "talk": {
        "text": "Kaile smiles faintly. Her eyes look tired, as if she hasn’t slept for days. 'Hey {name}' she answered,you approached her, you stood beside her, the silence ypu two shared was comforting. Time flies fast and it was now getting late, you decided to...",
        "image": "forest1.png",
        "character": "kylie.png",
        "choices": [
            {"text": "Invite her back to town", "next_scene": "go_back", "affection": -4, "courage": -2},
            {"text": "Stay and explore the forest with her", "next_scene": "explore", "affection": +6, "courage": +4}
        ]
    },

    "avoid": {
        "text": "You walk away, but the feeling of being watched lingers. The forest whispers your name...{name}...your name echoed through the silent forest accompanied by a small gust of wind. A strong feeling urges you to go back",
        "image": "forest1.png",
        "character": None,
        "choices": [
            {"text": "Go back and talk to Kaile", "next_scene": "talk", "affection": +2, "courage": +1},
            {"text": "Keep walking home", "next_scene": "end_coward", "affection": -100, "courage": -10}
        ]
    },

    "go_back": {
        "text": "You and Kaile head back toward town. The air feels lighter, but she suddenly stops. 'Thank you for walking with me,' she says softly. Her eyes looked tired",
        "image": "forest1.png",
        "character": "kaile_confess.png",
        "choices": [
            {"text": "Smile and keep walking", "next_scene": "end_friends", "affection": +2, "courage": 0},
            {"text": "Ask if she’s okay", "next_scene": "confess_scene", "affection": +3, "courage": +4}
        ]
    },

    "explore": {
        "text": "The two of you explore deeper. You hear strange noises... something is following you. Fear slowly crept into you. You looked at Kaile and she seemed unfazed, so you...",
        "image": "forest1.png",
        "character": None,
        "choices": [
            {"text": "Run back to town!", "next_scene": "escape", "affection": +1, "courage": +1},
            {"text": "Explore the forest (maze)", "next_scene": "minigame_result"}
        ]
    },

    "minigame_result": {
        "text": "(You played the maze minigame...)",
        "image": "forest1.png",
        "character": None,
        "auto": True
    },

    "event": {
        "text": "A rustling sound... Kaile’s face suddenly changes shape for a split second. 'Am I hallucinating?' you thought to yourself.",
        "image": "forest.jpg",
        "character": "kaile_aswang_hint.png",
        "choices": [
            {"text": "Ask what’s wrong", "next_scene": "confess_scene", "affection": +4, "courage": +2},
            {"text": "Pretend you saw nothing", "next_scene": "end_denial", "affection": -2, "courage": -2}
        ]
    },

    "escape": {
        "text": "You run as fast as you can. Your heart pounding as fear continued to suffocate your mind. The air smells like blood...",
        "image": "Death.png",
        "character": None,
        "choices": [
            {"text": "Hide inside an old hut", "next_scene": "end_hunter", "affection": 0, "courage": +3,"image": "oldhut.jpg",}
        ]
    },

    "confess_scene": {
        "text": " 'Are you alright Kaile' you asked her curiously,she nods, smiling at you. 'Im okay now that you're, {name}'. The place was beautiful, you felt it was the perfect moment. 'Kaile ive...actually liked you for awhile now...' here Kaile looks surprised. Her eyes shimmer. 'You... really mean it?'",
        "image": "forest1.png",
        "character": "kaile_confess.png",
        "choices": [
            {"text": "Yes... I’ve loved you for a long time.", "next_scene": "ending_check", "affection": +8, "courage": +6},
            {"text": "Forget it, it’s nothing.", "next_scene": "end_reject", "affection": -3, "courage": -1}
        ]
    },

    # Endings
    "end_coward": {
        "text": "You never saw Kaile again. Sometimes, in your dreams, you hear her calling your name. But you never had the courage to return.",
        "image": "end_coward.png",
        "character": None,
        "choices": []
    },

    "end_friends": {
        "text": "Kaile thanks you for always being there. You remain close friends for years, though something unspoken lingers,seemingly your unrevealed feelings.",
        "image": "pg.png",
        "character": None,
        "choices": []
    },

    "end_reject": {
        "text": "Kaile looks down. 'I’m sorry. I can’t return those feelings.' That night, your heart aches more than any wound could.You felt disappointed,defeated even.",
        "image": "Death.png",
        "character": None,
        "choices": []
    },

    "end_denial": {
        "text": "You try to live normally, but the truth gnaws at you. Sometimes you think you see Kaile’s eyes glowing red in the dark.",
        "image": "Death.png",
        "character": None,
        "choices": []
    },

    "end_hunter": {
        "text": "Years later, you became known as the Aswang Hunter of Kakako — determined to find the truth behind Kaile’s disappearance.",
        "image": "hunter.png",
        "character": None,
        "choices": []
    },

   "good": {
    "text": "Kaile smiles and embraces you. Her curse fades under the warmth of your courage and love. You felt at ease, and relaxed and glad that you saved her.",
    "image": "goodoyG.png",
    "character": None,
    "choices": []
},

    "best": {
        "text": "Together you lift the curse and become legends. Kakako remembers your bravery for generations.",
        "image": "goud.png",
        "character": None,
        "choices": []
    },

    "rejection": {
        "text": "The pain of lost love lingers. You live but never fully recover from that one night.You missed her deeply.",
        "image": "Rejection.png",
        "character": None,
        "choices": []
    },

    "death": {
        "text": "Your body collapses beneath the trees deep in the forest where nobody could find you. The forest keeps another secret.",
        "image": "Death.png",
        "character": None,
        "choices": []
    }
}