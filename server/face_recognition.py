import cv2
import dlib
import numpy as np

class FaceRecognition :
	'''
	To recognise the faces of people in a photo or video
	'''

	def __init__(self):
		'''
		Loading up the weights for the neural nets.
		'''
		self.detectorSimple = dlib.get_frontal_face_detector()
		self.predictor = dlib.shape_predictor('models_weights/shape_predictor.dat')
		self.detectorCNN = dlib.cnn_face_detection_model_v1('models_weights/face_detector.dat')
		self.face_encoder = dlib.face_recognition_model_v1('models_weights/face_recognition.dat')

	def _rect_to_css(self, rect):
		'''
		Convert a dlib rectangle to a tuple having (top, right, bottom, left) order

		Input : 
		rect:a dlib 'rect' object

		Output:
		A tuple having (top, right, bottom, left) 
		'''

		return (rect.top(), rect.right(), rect.bottom(), rect.left())

	def _css_to_rect(self, css) :
		'''
		Convert a tuple into a dlib 'rect' object

		Input:
		tuple in order (top, right, bottom, left)

		Output:
		a dlib 'rect' object
		'''
		return dlib.rectangle(css[3], css[0], css[1], css[2])

	def _trim_css_to_bounds(self, css, image_shape):
		"""
		Make sure a tuple in (top, right, bottom, left) order is within the bounds of the image.
		:param css:  plain tuple representation of the rect in (top, right, bottom, left) order
		:param image_shape: numpy shape of the image array
		:return: a trimmed plain tuple representation of the rect in (top, right, bottom, left) order
		"""
		return max(css[0], 0), min(css[1], image_shape[1]), min(css[2], image_shape[0]), max(css[3], 0)

	def load_image_file(self, file):
		'''
		Load an image file into a numpy array object

		Input:
		file: path for the image to load

		Output:
		Return a numpy object having image contents
		'''
		return cv2.imread(file)

	def face_distance(self, face_encodings, face_to_compare):
		"""
		Given a list of face encodings, compare them to a known face encoding and get a euclidean distance
		for each comparison face. The distance tells you how similar the faces are.
		:param faces: List of face encodings to compare
		:param face_to_compare: A face encoding to compare against
		:return: A numpy ndarray with the distance for each face in the same order as the 'faces' array
		"""
		if len(face_encodings) == 0:
		    return np.empty((0))

		return np.linalg.norm(face_encodings - face_to_compare, axis=1)

	def _raw_face_locations(self, img, upsampling=1, model="hog"):
		'''
		Returns an array of bounding boxes of human faces in image

		Input:
		img: An image as numpy array
		upsampling: How many times to upsample image to find small faces
		model: face detection model "hog" is less accurate but faster(preferred on CPU). "cnn" is more accurate model but slower so use it on GPU )

		Output:
		A list of dlib 'rect' objects for each found face
		'''

		if model == "hog":
			return self.detectorSimple(img, upsampling)
		else:
			return self.detectorCNN(img, upsampling)

	def face_locations(self, img, upsampling=1, model='hog'):
		''' 
		Returns an array of bounding boxes of human faces in image

		Input:
		img: An image as numpy array
		upsampling: How many times to upsample image to find small faces
		model: face detection model. "hog" is less accurate but faster(preferred on CPU). "cnn" is more accurate model but slower so use it on GPU )

		Output:
		A list of tuples for each found face in (top, right, bottom, left) order
		'''
		if model == 'hog':
			return [self._trim_css_to_bounds(self._rect_to_css(face), img.shape) for face in self._raw_face_locations(img, upsampling, model)]
		else:
			return [self._trim_css_to_bounds(self._rect_to_css(face.rect), img.shape) for face in self._raw_face_locations(img, upsampling, model)]


	def _raw_face_landmarks(self, img, model):
		'''
		Returns face landmarks used to properly align the face for face_recognition_model_v1

		Input:
		face_img: image of face to search
		model: face detection model.

		Output:
		Return all 68 landmarks as a list of dlib coordinates objects 
		'''
		return [self.predictor(img, face_location) for face_location in self._raw_face_locations(img, model=model)]

	def face_encodings(self, img, model='hog', num_jitter=1):
		'''
		Given an Image, return the 128-dimension face encoding for each face in image

		Input:
		img: The image that contains one or more faces
		num_jitter: How many times to resample the image while calculating encoding
		model: face detection model.

		Output:
		Return a list of numpy array of 128-dimensional face encoding.
		'''
		raw_ladmarks = self._raw_face_landmarks(img, model)

		return [np.array(self.face_encoder.compute_face_descriptor(img, raw_ladmarks_set, num_jitter)) for raw_ladmarks_set in raw_ladmarks]

	def compare_faces(self, known_face_encodings, face_encoding_to_check, tolerance=0.55):
		"""
		Compare a list of face encodings against a candidate encoding to see if they match.
		:param known_face_encodings: A list of known face encodings
		:param face_encoding_to_check: A single face encoding to compare against the list
		:param tolerance: How much distance between faces to consider it a match. Lower is more strict. 0.6 is typical best performance.
		:return: A list of True/False values indicating which known_face_encodings match the face encoding to check
		"""
		distances = self.face_distance(known_face_encodings, face_encoding_to_check)
		return list( distances <= tolerance)
