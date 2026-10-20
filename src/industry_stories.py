"""Story-led industry content: the Indian reality, what goes wrong, how UBM fixes it.

Stats carry their source so every number on the site can be checked.
Pain points are drawn from recurring questions on Reddit (r/india, r/sysadmin, r/k12sysadmin,
r/livesound, r/hometheater) and Quora, rewritten in plain language.
"""

STORIES = {
"education": {
 "story": "Walk into most Indian schools today and you will find a smart board somewhere. Walk in again a year later and many of them are being used as an expensive projector screen, or not at all. The problem is rarely the idea of digital learning. It is screens that wash out in daylight, boards that need calibrating before every period, teachers who were never trained, and a supplier who takes three weeks to send a technician. UBM has been fixing exactly these problems for Indian schools, colleges and universities since 1997.",
 "stats": [
  ("64.7%", "of Indian schools have computers, and 63.5% have internet (UDISE+ 2024-25)", "Ministry of Education, Lok Sabha reply", "https://www.education.gov.in/sites/upload_files/mhrd/files/parliament_annexure_en/LSUQ_4920_en.pdf"),
  ("58%", "of schools have computers that actually work for teaching, analysts estimate from the same data", "Education for All in India, UDISE+ analysis", "https://educationforallinindia.com/school-infrastructure-insights-from-udise-2024-25/"),
  ("1 in 3", "schools still have no internet, so classroom technology must work offline as well as online", "UDISE+ 2024-25", "https://www.education.gov.in/sites/upload_files/mhrd/files/parliament_annexure_en/LSUQ_4920_en.pdf"),
 ],
 "pains": [
  ("“We bought smart boards. Nobody uses them.”", "The most common complaint from principals and teachers online. Slow start-up, calibration and missing training turn a ₹1-lakh investment into a wall decoration."),
  ("Screens you can't see in daylight", "Indian classrooms have big windows and rarely have blackout. Older projectors wash out by mid-morning, so teachers switch them off."),
  ("Back benches can't see or hear", "A 65-inch panel in a 45-student room, and no audio, means the last three rows miss half the lesson."),
  ("Service takes weeks", "When a panel fails mid-term, many schools wait weeks for a technician from another city."),
 ],
 "fixes": [
  ("Daylight-proof displays", "Interactive flat panels for bright classrooms; high-brightness laser projectors for lecture halls where size matters more than touch."),
  ("Sized for the last row", "We size every screen to the farthest student and add voice-lift audio in rooms over 40 students."),
  ("Training that sticks", "Hands-on teacher training at handover, a champion teacher in every school, and refresher sessions each term."),
  ("Support from Mumbai", "A team you can reach, spares and warranty handled for you, and standardised designs that are easy to maintain."),
 ],
 "project": ["Free site survey of your classrooms and halls", "Room-by-room design and an itemised proposal", "Installation outside school hours", "Teacher training and handover", "Preventive maintenance each term"],
 "faqs": [
  ("What does a smart classroom need in an Indian school?", "An interactive display sized for the room, wireless sharing, audio for larger classes, a document camera, proper mounting and power, and teacher training."),
  ("Can installation happen without disturbing classes?", "Yes. UBM schedules installation after school hours, on weekends or during vacations."),
  ("Do smart classrooms work without internet?", "Yes. Interactive panels and projectors work offline for teaching; internet adds online content and updates."),
 ],
},
"corporate": {
 "story": "Every Indian office has the same five minutes at the start of a meeting: someone hunting for the right HDMI adapter, the remote team saying “you're on mute”, the CEO's voice echoing off the glass walls. Multiply that by every meeting, in every room, every day, and it is a serious cost. As global capability centres and hybrid teams reshape India's offices, meeting rooms have become the place where work is either won or wasted. UBM designs rooms where the meeting starts the moment people walk in.",
 "stats": [
  ("32.5M sq ft", "of office space leased by global capability centres in India's top 7 cities in 2025, out of 80.5M sq ft", "FICCI-ANAROCK via PTI", "https://psuwatch.com/newsupdates/pti/biz-realty-office"),
  ("$64 bn", "size of India's GCC market in 2024, projected to reach $105-110 bn by 2030", "FICCI-ANAROCK via IANS", "https://ianslive.in/indias-gcc-market-to-touch-110-bn-growing-10-pc-annually-through-2030--20260203132410"),
  ("12.35%", "projected annual growth of India's video conferencing market, 2025-2033", "Market research summary", "https://marketresearchreports.notion.site/India-Video-Conferencing-Market-Size-Share-and-Trends-2025-2033-1ec6eb08b55980f2a1c5ed57b07d82d0"),
 ],
 "pains": [
  ("“You're on mute” and echo", "IT managers on r/sysadmin say audio is the number-one meeting-room complaint. Glass cabins popular in Indian offices make echo worse."),
  ("Every room works differently", "Different equipment in every room means staff never learn any of them, and IT supports ten designs instead of one."),
  ("Hunting for cables", "Guests arrive with USB-C, HDMI and Mac laptops. Without wireless sharing, meetings start late."),
  ("Remote people can't see the room", "A laptop camera at one end of a long table shows remote colleagues a row of shoulders."),
 ],
 "fixes": [
  ("Audio designed first", "Ceiling or table microphones that cover every seat, conferencing loudspeakers and acoustic treatment for glass rooms."),
  ("Small, medium, large standards", "One design per room size, rolled out identically across floors and cities."),
  ("One-tap start", "Wireless sharing and certified Teams, Zoom or Meet room systems so meetings start on time."),
  ("Cameras that frame the room", "Auto-framing and speaker-tracking cameras so remote colleagues see who is talking."),
 ],
 "project": ["Audit of existing rooms and meeting habits", "Room standards and a phased roll-out plan", "Installation floor by floor, after hours", "User training and IT handover", "AMC with response times in writing"],
 "faqs": [
  ("Why is audio the biggest problem in meeting rooms?", "Remote participants judge a meeting by what they hear. Poor microphone coverage and echo from glass walls are the most common causes."),
  ("Can you upgrade our existing rooms instead of replacing everything?", "Yes. We reuse what still works and usually upgrade audio and wireless sharing first."),
  ("Do you support offices outside Mumbai?", "Yes. UBM supports offices across India directly and through partner integrators."),
 ],
},
"hospitality": {
 "story": "India's wedding season alone now moves more money than many industries do in a year, and almost every rupee of it passes through a banquet hall, a ballroom or a lawn. Guests remember the décor, the food and whether they could hear the speeches. Banquet managers remember the nights the microphone cut out during the sangeet, or the projector washed out during the couple's video. UBM designs hotel and banquet AV that sounds as good as the venue looks, and is simple enough for the night staff to run.",
 "stats": [
  ("46 lakh", "weddings expected in India's 2025 wedding season alone (1 Nov-14 Dec)", "CAIT", "https://cait.in/wedding-season-2025-to-generate-₹6-5-lakh-crore-business-from-46-lakh-weddings-across-india-cait-delhi-alone-to-witness-₹1-8-lakh-crore-trade-from-4-8-lakh-weddings-indian/"),
  ("₹6.5 lakh crore", "of trade generated by that single wedding season, up from ₹5.9 lakh crore in 2024", "CAIT", "https://cait.in/wedding-season-2025-to-generate-₹6-5-lakh-crore-business-from-46-lakh-weddings-across-india-cait-delhi-alone-to-witness-₹1-8-lakh-crore-trade-from-4-8-lakh-weddings-indian/"),
  ("4.8 lakh", "weddings in Delhi alone in the 2025 season, worth about ₹1.8 lakh crore", "CAIT", "https://cait.in/wedding-season-2025-to-generate-₹6-5-lakh-crore-business-from-46-lakh-weddings-across-india-cait-delhi-alone-to-witness-₹1-8-lakh-crore-trade-from-4-8-lakh-weddings-indian/"),
 ],
 "pains": [
  ("Speeches nobody can hear", "Two big speakers at the stage end of a long hall: deafening at the front, mumbling at the back."),
  ("Feedback and dropouts", "Cheap wireless microphones squeal and cut out, right during the toast."),
  ("Every DJ brings their own rig", "Without proper input plates and a house system, every event means cables across the floor."),
  ("Partitions break the sound", "When a ballroom is split into two halls, music and announcements leak from one event into the other."),
 ],
 "fixes": [
  ("Even coverage, every table", "Distributed or column speakers designed so every guest hears clearly, without blasting the front rows."),
  ("Reliable wireless microphones", "Professional handheld and lapel microphones with proper frequency planning."),
  ("Plug-and-play for DJs and bands", "Input plates around the hall feeding a house system the venue controls."),
  ("Divisible-room presets", "One button switches the ballroom between one big event and two separate ones."),
 ],
 "project": ["Venue walk-through during a live event", "Coverage design for halls, lawns and pre-function areas", "Installation between bookings", "Staff training with simple presets", "Season-ready maintenance before peak dates"],
 "faqs": [
  ("What sound system does a banquet hall need?", "A distributed or column speaker system designed for even coverage, professional wireless microphones, input plates for DJs and bands, and simple presets for staff."),
  ("Can you work around our booking calendar?", "Yes. Installation is scheduled between bookings and before peak wedding dates."),
 ],
},
"places-of-worship": {
 "story": "India has more places of worship than schools and colleges combined. Each one is acoustically unique: stone mandapams that ring for seconds, domes that swallow speech, and courtyards where thousands gather on festival days. Most still rely on a single amplifier and a pair of horn speakers that are too loud near the entrance and inaudible in the hall. At the same time, noise rules mean loudspeakers must be controlled after 10 pm. UBM helps trusts and committees get every word heard inside, without disturbing the neighbourhood outside.",
 "stats": [
  ("30 lakh+", "places of worship in India, more than the 21 lakh schools and colleges", "Census 2011, via Humans of Data", "https://humansofdata.atlan.com/2016/07/real-numbers-places-worship-schools-colleges-india"),
  ("6.48 lakh", "temples mapped across India in one 2022 survey", "Temples of India survey, reported by South First", "https://thesouthfirst.com/?p=220227"),
  ("10 pm-6 am", "loudspeakers and PA systems may not be used outdoors in this window, under India's Noise Pollution Rules, 2000 (limited exemptions apply)", "Noise Pollution (Regulation and Control) Rules, 2000", ""),
 ],
 "pains": [
  ("Echo swallows the words", "Stone and marble halls reverberate so much that pravachans, kirtans and sermons become hard to follow."),
  ("Loud outside, quiet inside", "Horn speakers on the roof reach the street but not the back of the hall, which also invites noise complaints."),
  ("Festival-day crowds", "Daily systems can't cope when thousands gather for Navratri, Eid, Christmas or Gurpurab."),
  ("Volunteers run the system", "Committees rely on volunteers, so complicated mixers lead to feedback and mistakes."),
 ],
 "fixes": [
  ("Directional speakers for clarity", "Column and steerable speakers aim sound at devotees and away from reflective walls."),
  ("Inside-first design", "Sound is designed for the hall first, with controlled outdoor zones that can be scheduled to respect noise rules."),
  ("Festival-ready capacity", "Overflow zones, courtyard speakers and screens that switch on for big days."),
  ("One-button presets", "Daily aarti, discourse and festival modes so volunteers can run it confidently."),
 ],
 "project": ["Acoustic visit during a regular prayer or service", "Speaker placement plan respecting the architecture", "Discreet installation that preserves the décor", "Volunteer training with presets", "Support before every major festival"],
 "faqs": [
  ("Why is sound unclear in temples, churches and mosques?", "Hard stone and marble surfaces and high ceilings cause echo. Directional speakers placed correctly make speech clear."),
  ("Can the system respect noise regulations?", "Yes. Indoor sound can be prioritised and outdoor zones scheduled or limited in line with applicable rules."),
  ("Can installation preserve the architecture?", "Yes. We choose discreet speakers and cable routes that respect the building."),
 ],
},
"stadiums-sports-venues": {
 "story": "India is building sports venues at a scale few countries match, from the world's largest cricket stadium in Ahmedabad to new multi-sport complexes in tier-2 cities. Fans now expect the same experience they see on TV: clear announcements, replays on big screens and hospitality boxes that feel premium. Behind the scenes, venue teams want to run all of it from one control room with a small crew. UBM brings networked sound, screens and control to venues that host thousands.",
 "stats": [
  ("1,32,000", "seats at the Narendra Modi Stadium, Ahmedabad, the world's largest cricket stadium", "President of India, press release", "https://ramnathkovind.nic.in/pr240221.html"),
  ("68,000", "approximate capacity of Eden Gardens, Kolkata", "GKToday venue list", "https://www.gktoday.in/famous-cricket-stadiums-in-india/"),
  ("33,108", "approximate capacity of Wankhede Stadium, Mumbai", "GKToday venue list", "https://www.gktoday.in/famous-cricket-stadiums-in-india/"),
 ],
 "pains": [
  ("Announcements turn to mush", "In a huge bowl, delays between speakers make announcements echo and blur."),
  ("Screens in the wrong places", "Fans in the upper tiers and concourses miss replays and safety messages."),
  ("Too many control points", "Separate systems for the bowl, boxes and press rooms need a large crew on every match day."),
  ("Emergency messaging", "Evacuation announcements must be heard clearly everywhere, every time."),
 ],
 "fixes": [
  ("Zoned, time-aligned audio", "Speakers zoned and delayed correctly so every stand hears clear announcements."),
  ("Screens where fans are", "LED walls for the bowl and displays across concourses and boxes."),
  ("One control room", "AV over IP and central control so a small crew runs the whole venue."),
  ("Priority paging", "Emergency messages override everything, across every zone."),
 ],
 "project": ["Venue survey on a match or event day", "Zoning and screen-placement design", "Phased installation between seasons", "Control-room training", "Match-day support plans"],
 "faqs": [
  ("Why use networked AV in a stadium?", "It lets a small team control sound and screens across the whole venue from one place, and scales as zones are added."),
  ("Can new systems work with existing infrastructure?", "Often yes. We assess what can be reused and integrate new zones in phases."),
 ],
},
"home-theatre": {
 "story": "Indian homes are falling in love with the big screen again, but at home. The weekend IPL match, the new OTT series, the family movie night: people want the cinema feeling without the cinema queue. The trouble usually starts after the interiors are finished, when there is no cable route, no place for rear speakers and a projector that washes out because the room was never planned for it. UBM designs home theatres in Mumbai with homeowners and their architects, before the first wall is painted.",
 "stats": [
  ("$457.9M", "size of India's home theatre market in 2024, projected to reach $2.18 bn by 2033", "IMARC Group", "https://www.imarcgroup.com/india-home-theater-market"),
  ("18.9%", "projected annual growth of India's home theatre market, 2025-2033", "IMARC Group", "https://www.imarcgroup.com/india-home-theater-market"),
  ("2x by 2029", "BenQ India expects the home projector category to double, led by South and West India", "BenQ India MD, via Madhyamam", "https://madhyamamonline.com/amp/business/indias-home-projector-market-set-to-double-by-2029-1410345"),
 ],
 "pains": [
  ("Planned after the interiors", "No conduits, no speaker positions and no ceiling mount, so everything ends up on show."),
  ("Washed-out picture", "Living rooms with big windows and light walls kill projector contrast."),
  ("Booming bass, muddy dialogue", "Bare walls and hard floors make dialogue hard to follow at sensible volumes."),
  ("Power cuts and dust", "Projectors and amplifiers need surge protection, backup and ventilation in Indian conditions."),
 ],
 "fixes": [
  ("Plan with your architect", "Cable routes, ceiling mounts and speaker positions designed before interiors are finished."),
  ("Right screen, right projector", "Projector or large display chosen for your room's light, with the screen sized to your seating."),
  ("Room-aware sound", "Speaker placement and simple acoustic treatment for clear dialogue and controlled bass."),
  ("Built for Indian homes", "Surge protection, UPS planning and dust-aware equipment choices."),
 ],
 "project": ["Home visit with you and your architect", "Layout, screen and speaker plan", "Pre-wiring during interiors", "Final installation and calibration", "One-remote setup and handover"],
 "faqs": [
  ("When should I plan my home theatre?", "Before interiors are finished, so cables, mounts and speaker positions can be concealed."),
  ("Projector or TV for my home theatre?", "A projector gives a far bigger picture for the money if light can be controlled; a large TV suits bright living rooms."),
 ],
},
"retail": {
 "story": "Indian shoppers walk past hundreds of brands in a single mall visit. The stores that stop them are the ones that move: a window that changes with the season, a video wall that tells a story, music that matches the brand. Yet many retailers still run USB sticks into TVs and update content by sending someone to every store. UBM helps retailers, showrooms and malls build displays and sound that look premium and can be managed centrally.",
 "stats": [
  ("$1.07 bn", "size of India's digital signage market in 2025, projected to reach $3.49 bn by 2034", "IMARC Group", "https://www.imarcgroup.com/india-digital-signage-market"),
  ("14%", "projected annual growth of India's digital signage market, 2026-2034", "IMARC Group", "https://www.imarcgroup.com/india-digital-signage-market"),
  ("16.6M sq ft", "of new prime mall space due across India's seven major cities by 2026", "P&S Intelligence", "https://www.psmarketresearch.com/market-analysis/india-commercial-display-market-report"),
 ],
 "pains": [
  ("USB-stick signage", "Content updated by hand, store by store, means old offers stay on screen for weeks."),
  ("Screens that disappear in daylight", "Consumer TVs in shop windows are too dim to compete with Indian sunlight."),
  ("Music that doesn't fit", "One volume for the whole store: too loud at the till, too quiet in the fitting rooms."),
  ("Displays that fail early", "Consumer screens running 14 hours a day are not built for retail duty."),
 ],
 "fixes": [
  ("Central content control", "Update every store's screens from one place, on a schedule."),
  ("Window-grade brightness", "High-brightness commercial displays and LED for windows and atriums."),
  ("Zoned background music", "Separate zones and volumes for the floor, tills and fitting rooms."),
  ("Commercial-grade hardware", "Displays rated for long daily operation, with warranty handled for you."),
 ],
 "project": ["Store or mall walk-through", "Display and audio plan per format", "Installation outside trading hours", "Content and control training", "Multi-store support"],
 "faqs": [
  ("Can signage across many stores be controlled centrally?", "Yes. Screens can be scheduled and updated centrally across locations."),
  ("Why not use regular TVs for store displays?", "Commercial displays are brighter and built for long daily operation; consumer TVs are not."),
 ],
},
}
