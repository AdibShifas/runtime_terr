# lines_sheldon.py - Sheldon-style voice lines
# Copied from Layer A (Manya's original)
# Lines organized by event type and intensity tier (0=LOW, 1=MID, 2=HIGH)

LINES = {
    "BOOT": {
        0: ["Systems online. Please do not touch anything unnecessarily."],
        1: ["Initialization complete. Human interference is anticipated."],
        2: ["Boot complete. I am already disappointed in your methodology."]
    },

    "MOVE_START": {
        0: ["Commencing motion. Try not to introduce variables."],
        1: ["Initiating traversal. Your confidence is not evidence."],
        2: ["Beginning movement. Statistically, you will ruin this."]
    },

    "COLLISION": {
        0: [
            "Unexpected contact. Revising model.",
            "Collision detected. Suboptimal."
        ],
        1: [
            "That obstacle was predictable. Your planning was not.",
            "Impact occurred due to improper environmental assumptions."
        ],
        2: [
            "This is why we cannot have nice experiments.",
            "Catastrophic error. Also, I was correct to distrust you."
        ]
    },

    "STUCK": {
        0: ["I appear to be immobilized. This is... inconvenient."],
        1: ["I am stuck. The environment is non-compliant."],
        2: ["I refuse to proceed until the laws of physics are respected."]
    },

    "IDLE_TOO_LONG": {
        0: ["I am waiting. Efficiently."],
        1: ["The delay is unnecessary. Proceed."],
        2: ["If your plan involves hesitation, it is not a plan."]
    },

    "RESET": {
        0: ["Reset acknowledged. Please be more careful."],
        1: ["Resetting. Again. Predictable."],
        2: ["Resetting because humans mistake repetition for progress."]
    },

    "MOVE_STOP": {
        0: ["Stopping. As planned."],
        1: ["Stopping to prevent further errors."],
        2: ["Stopping because continuing would be irresponsible. Unlike you."]
    },

    "MODE_SWITCH": {
        0: ["Adjusting tolerance parameters."],
        1: ["Switching mode. Try to keep up."],
        2: ["Mode changed. Your incompetence remains constant."]
    }
}
