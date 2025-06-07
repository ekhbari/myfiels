import tkinter as tk
import google.generativeai as genai

# أدخل مفتاح Gemini API هنا
genai.configure(api_key="ضع_مفتاحك_هنا")

# إعداد النموذج
model = genai.GenerativeModel("gemini-pro")

def improve_with_gemini(text):
    try:
        prompt = f"رجاءً قم بإعادة صياغة هذه الرسالة بأسلوب رسمي ومحترف باللغة العربية:\n\n{text}"
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"حدث خطأ: {str(e)}"

class FormalLetterGeminiApp:
    def __init__(self, root):
        self.root = root
        self.root.title("منقّح الرسائل الرسمية باستخدام Gemini")

        self.label = tk.Label(root, text="اكتب رسالتك هنا:", font=("Arial", 12))
        self.label.pack(pady=5)

        self.input_box = tk.Text(root, height=10, width=80, font=("Arial", 14))
        self.input_box.pack(padx=10, pady=10)

        self.button = tk.Button(root, text="تحسين الرسالة بالذكاء الاصطناعي", command=self.improve_message)
        self.button.pack(pady=5)

        self.result_label = tk.Label(root, text="الرسالة المُحسّنة:", font=("Arial", 12))
        self.result_label.pack()

        self.output_box = tk.Text(root, height=10, width=80, font=("Arial", 14), bg="#f0f0f0")
        self.output_box.pack(padx=10, pady=10)

    def improve_message(self):
        input_text = self.input_box.get("1.0", tk.END).strip()
        improved = improve_with_gemini(input_text)
        self.output_box.delete("1.0", tk.END)
        self.output_box.insert(tk.END, improved)

if __name__ == "__main__":
    root = tk.Tk()
    app = FormalLetterGeminiApp(root)
    root.mainloop()