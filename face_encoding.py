import face_recognition

ref_img_one = face_recognition.load_image_file("rahul.jpg")
ref_img_face_encodings_one = face_recognition.face_encodings(ref_img_one)

ref_img_two = face_recognition.load_image_file("Charan.jpg")
ref_img_face_encodings_two = face_recognition.face_encodings(ref_img_two)

# Ensure encodings are not empty
known_face_encodings = [
    ref_img_face_encodings_one[0],
    ref_img_face_encodings_two[0]
]

known_face_names = [
    "Sneha",
    "Charan"
]
