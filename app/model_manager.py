import xgboost as xgb
import os

class ModelManager:
    def __init__(self, model_path: str):
        self.model_path = model_path
        self.model = xgb.XGBClassifier()
        self._load()

    def _load(self):
        if os.path.exists(self.model_path):
            self.model.load_model(self.model_path)
            print(f"📦 Model loaded from {self.model_path}")
        else:
            raise FileNotFoundError(f"No found the model in {self.model_path}")

    def reload(self, new_path: str = None):
        target_path = new_path or self.model_path
        try:
            temp_model = xgb.XGBClassifier()
            temp_model.load_model(target_path)
            self.model = temp_model
            self.model_path = target_path
            return True
        except Exception as e:
            print(f"❌ Error to reload the model: {e}")
            return False

ModelManagerSingleton = ModelManager("app/model_sentinel.json")