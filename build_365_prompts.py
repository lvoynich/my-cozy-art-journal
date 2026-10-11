import json

# Curating a diverse pool of classic Zentangle patterns and creative prompts
base_prompts = [
    "Draw 'Printemps' (tight spirals) starting from the center outward.",
    "Try 'Hollibaugh' (overlapping planks) to create a woven layered grid.",
    "Draw 'Crescent Moon' by nesting curves around dark crescent shapes.",
    "Fill a corner with 'Knightsbridge' alternating black and white squares.",
    "Draw standard geometric lines, then use your highlighter to add a neon pop behind them.",
    "Focus on slow, steady line strokes today. Turn your brush stabilization up to 60%.",
    "Draw an irregular, organic 'string' shape using a looping line, then fill it.",
    "Try 'Florz'—a simple grid pattern with tiny diamond accents at the cross-sections.",
    "Color Drop a solid bright color into this entire box, then draw your patterns in black over it.",
    "Draw tiny, clustered 'Perles' (pearl circles) tracking along a single wavy line."
]

# EXPANDED ARRAY MATRIX: Adding more variables to multiply the math options
actions = [
    "Fill a section with", "Weave a cluster of", "Border your space using", 
    "Contrast thin lines with", "Draw a smooth matrix of", "Layer alternating rows of",
    "Divide the box organically and add", "Scatter a loose field of"
]

patterns = [
    "nested organic scales", "sharp geometric triangles", "tight concentric circles", 
    "wavy parallel ribbons", "intricate checkerboard blocks", "soft teardrop droplets",
    "clean parallel fine-lines", "bold overlapping zig-zags", "spiraling fractal mandalas"
]

styles = [
    "and use your eraser to create highlights.", "then shade the edges with a digital pencil tool.", 
    "keeping the layout ultra-minimalist.", "exploding with bright neon highlights.", 
    "and let them overlap chaotic lines underneath.", "using highly saturated primary colors.",
    "blending a soft pastel gradient behind them.", "maintaining perfect structural symmetry."
]

generated_prompts = []
# 8 actions x 9 patterns x 8 styles = 576 completely unique combinations!
for act in actions:
    for pat in patterns:
        for sty in styles:
            generated_prompts.append(f"{act} {pat} {sty}")

# Combine lists and slice exactly down to a full 365 calendar dataset
final_365_prompts = (base_prompts + generated_prompts)[:365]

with open("prompts.json", "w", encoding="utf-8") as f:
    json.dump(final_365_prompts, f, indent=2)

print(f"Success! Local data architecture built. Saved exactly {len(final_365_prompts)} unique prompts into prompts.json.")
