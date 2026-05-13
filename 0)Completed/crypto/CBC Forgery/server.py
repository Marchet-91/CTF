#!/usr/bin/env python3

import os
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad

flag = os.getenv("FLAG", "srdnlen{redacted}")

key = os.urandom(16)

target = """@everyone 
**A small personal rant about AI Slopping from an old player** (if you are interested read it without asking AI to summarize 😄  - otherwise feel free to skip - thank you!)

I apologize for using this space for expressing my personal thoughts, but it's something I have been thinking about for a while.

I have been playing CTFs for almost 10 years now, with the Sardinia Len team existing since 2019. We have played many competitions over the years, and organized various editions of Sardinia Len CTF (and Sardinia Cyber Camp). We have always had a tremendous amount of fun playing challenges and creating them. It's what united us and what makes are what we are (those who came to Sardinia met us and know what I mean).

However, this is the first time where, on a personal level, I feel that something is off. And not just because of my infamous third challenge (yes, there were at least two unintended and hard challenge creation skill issues from my side 😃), but because of the massive (and in most of the cases brainless) use of AI to solve challenges from players. I am personally not happy of what I am seeing from the community in general, and I honestly feel a bit disappointed.

During this CTF (and from many tickets), I saw many interesting things: from teams that slopped even tickets and requests, to others that obtained things that were not even able to interpret. Other teams even complained where something was difficult after having slopped 80% of the competition with AI.

I do not condemn those who are systematically using this technology (it was not even forbidden by the rules - so any reason is good). However, the question that, as a teacher and a captain of a CTF team, I ask to the community is: are you having fun? Does it make sense to do that? I started playing CTF to have fun and learn something. To keep my brain in shape and to have motivation from competition with my teammates.  This is also the reason that makes me create challenges as well: trying to share some knowledge and pushing you to learn more. And I ask you: What is your motivation? What pushes you? I think especially very young people should ask themselves this question and find a proper answer (whatever that is).

I personally notice that this enthusiasm is slowly disappearing. The problem is not AI itself (for many things, it's becoming very similar to using engines in chess...which is already considered cheating), but the uncontrolled use that it is done (even by ourselves at times). Sometimes I personally feel like a monkey (yes, I personally fell in the slopping trap myself more than once) that presses buttons and watches a screen. And I feel we are breaking the toy (or is it already broken?). When I see people reaching our final events by only slopping, I honestly feel a bit defeated. This is not what CTFs are. If you solve a Crypto challenge because you are good at sending prompts, you are NOT a Crypto expert. And this is not, in my personal opinion, what CTFs are testing. 

I do not have a proper solution for that. On the one hand, things will become worse and worse as models improve. On the other hand, I am positive the community will find something else to counteract. For sure, in our events in person, we are going to strongly limit from now on the use of AI. 

I hope this small text gives you all some food for thought. What I love and hope to see again, is the the spark of the fight when you struggle in solving the challenges that make yourself a better player - and person.

Thank you if you had the patience to read this and thank you again for playing ❤️
""".encode()

while True:
    try:
        ct = bytes.fromhex(input("your ciphertext: "))
    except ValueError:
        print("ciphertext needs to be hex encoded!")
    
    iv, ct = ct[:16], ct[16:]

    pt = AES.new(key, AES.MODE_CBC, iv).decrypt(ct)
    
    if pad(target, 16) == pt:
        print(f"hope you didn't slop this 🙏! {flag = }")
        break
    else:
        print(f":( {pt.hex() = }")
