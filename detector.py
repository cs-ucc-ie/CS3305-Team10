from pathlib import Path
from collections import Counter
import face_recognition
import pickle

DEFAULT_ENCODINGS_PATH = Path("output/encodings.pkl")

Path("training").mkdir(exist_ok=True)
Path("output").mkdir(exist_ok=True)
Path("validation").mkdir(exist_ok=True)


def encode_known_faces (
    model: str = "cnn", encodings_location: Path = DEFAULT_ENCODINGS_PATH
    ) -> None:
    names = []
    encodings = []
    for filepath in Path("training").glob("*/*"):
        name = filepath.parent.name
        image = face_recognition.load_image_file(filepath)

        face_locations = face_recognition.face_locations(image, model=model)
        face_encodings = face_recognition.face_encodings(image, face_locations)
        
        for encoding in face_encodings:
            names.append(name)
            encodings.append(encoding)
            
    name_encodings = {"names":names, "encodings":encodings}
    with encodings_location.open(mode="wb") as f:
        pickle.dump(name_encodings,f)

            
            
            
def recognize_faces(
    image_location: str,
    model: str = "cnn",
    encodings_location: Path = DEFAULT_ENCODINGS_PATH,
) -> None:
    with encodings_location.open(mode="rb") as f:
        loaded_encodings = pickle.load(f)
        
        
    input_image = face_recognition.load_image_file(image_location)
    
    
    input_face_locations = face_recognition.face_locations(input_image, model=model)
    input_face_encodings = face_recognition.face_encodings(input_image, input_face_locations)
    
    
    for bounding_box, unknown_encoding in zip(input_face_locations, input_face_encodings):
        name = _recognize_face(unknown_encoding, loaded_encodings)
        if not name:
            name = "Unknown"
        print(name, bounding_box)
        
        
def _recognize_face(unknown_encoding, loaded_encodings):
    boolean_matches = face_recognition.compare_faces(
        loaded_encodings["encodings"], unknown_encoding
    )
    votes = Counter(name for match, 
                    name in zip(boolean_matches, loaded_encodings["names"]) 
                    if match)
    
    if votes:
        return votes.most_common(1)[0][0]
    
recognize_faces("unknown.jpg")