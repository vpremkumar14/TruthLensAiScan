import numpy as np

def generate_explanation(prediction, confidence, cam):
    explanation = []

    # Confidence
    if confidence > 0.9:
        explanation.append("The model is highly confident.")
    elif confidence > 0.7:
        explanation.append("The model is moderately confident.")
    else:
        explanation.append("The model is uncertain.")

    # Heatmap intensity
    high_focus = np.mean(cam > 0.6)

    if prediction == "FAKE":
        explanation.append("The image shows signs of manipulation.")

        if high_focus > 0.3:
            explanation.append("Strong focus detected on facial regions like eyes or mouth.")

        explanation.append("Possible issues include unnatural skin texture, blending artifacts, or inconsistent lighting.")

    else:
        explanation.append("No strong manipulation patterns detected.")

        if high_focus < 0.2:
            explanation.append("The model did not detect suspicious regions.")

        explanation.append("Facial features appear natural and consistent.")

    return " ".join(explanation)