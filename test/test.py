from face2face import Face2Face
import cv2
from media_toolkit import VideoFile


f2f = Face2Face(device_id=1)
def test_single_face_swap():
    source_img = "test_imgs/test_face_1.jpg"
    target_img = "test_imgs/test_face_2.jpg"
    swapped = f2f.swap_one_image(source_img, target_img, enhance_face_model='gpen_bfr_2048')
    cv2.imwrite("test_swap.png", swapped)
#

def test_embedding_face_swap():
    source_img = "test_imgs/test_face_1.jpg"
    target_img = "test_imgs/test_face_2.jpg"
    f2f.add_face("hagrid", source_img, save=True)
    swapped = f2f.swap_to_face("hagrid", target_img)
    cv2.imwrite("test_swap.png", swapped)

def test_multi_face_from_reference():
    f1 = "test_imgs/test_face_1.jpg"
    f2 = "test_imgs/test_face_2.jpg"
    f3 = "test_imgs/test_face_3.png"
    f4 = "test_imgs/test_face_4.jpg"
    f2f.add_face("hagrid", f1, save=True)
    f2f.add_face("ron", f2, save=True)
    f2f.add_face("biden", f3, save=True)
    f2f.add_face("trump", f4, save=True)

    test_multi_face_img = "test_imgs/test_multi_swap_from_reference.jpg"
    swapped = f2f.swap_pairs(test_multi_face_img, swap_pairs={
        "trump": "hagrid",
        "biden": "ron"
    })
    cv2.imwrite("../docs/swap_with_recognition.jpg", swapped)

def test_video_face_swap():
    # add ref face
    source_img = cv2.imread("test_imgs/test_face_4.jpg")
    f2f.add_face("caprio", source_img, save=True)
    # swap it
    vf = VideoFile().from_file("test_imgs/smithy.mp4")
    swapped = f2f.swap_to_face_in_video(face_name="caprio", target_video=vf)
    swapped.save("test_imgs/test_video_2_swapped_swapped_smithy.mp4")

def test_multi_face_video_swap():
    # add ref face
    f2f.add_face("biden", "test_imgs/test_face_3.png", save=True)
    f2f.add_face("harris", "test_imgs/test_face_5.jpg", save=True)
    f2f.add_face("murphy", "test_imgs/test_face_6.jpg", save=True)
    f2f.add_face("warren", "test_imgs/test_face_7.jpeg", save=True)
    # swap it
    vf = VideoFile().from_file("test_imgs/test_video_1.mp4")
    swapped = f2f.swap_pairs_in_video(swap_pairs={
        "murphy": "biden",
        "warren": "harris"
    }, target_video=vf)
    swapped.save("test_imgs/z.mp4")


if __name__ == "__main__":

    test_multi_face_from_reference()
    test_multi_face_video_swap()