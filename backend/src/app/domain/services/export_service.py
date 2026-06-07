# apps/dataset_export/domain/exporters.py
import json
from typing import List

from app.db.models.dataset import DatasetCategory
from app.db.repositories.dataset_repository import DatasetRepository
from app.db.repositories.task_repository import TaskRepository
from app.domain.entities.export_schema import CompletedTaskData


class ExportService:
    def __init__(self, export_repo: TaskRepository, dataset_repo: DatasetRepository):
        self._task_repo = export_repo
        self._dataset_repo = dataset_repo

    def execute(self, dataset_id: int, format_type: str) -> bytes:
        raw_tasks = self._task_repo.get_completed_tasks_annotations(dataset_id)
        dataset_categories = self._dataset_repo.get_categories_by_dataset(dataset_id)

        completed_tasks = []
        for item in raw_tasks:
            annotation_data = item.get("annotation")

            if isinstance(annotation_data, dict):
                shapes = annotation_data.get("items", [])
            else:
                shapes = annotation_data or []

            completed_tasks.append(
                CompletedTaskData(
                    task_id=item["task_id"],
                    image_path=item["image"],
                    shapes=shapes,
                    width=item["width"],
                    height=item["height"],
                )
            )

        if format_type.lower() == "coco":
            exporter = COCOExporter()
            json_string = exporter.format(completed_tasks, dataset_categories)
            return json_string.encode("utf-8")


class COCOExporter:
    def format(self, completed_tasks: List[CompletedTaskData], dataset_categories: List[DatasetCategory]) -> str:
        coco_data = {"images": [], "annotations": [], "categories": []}

        for category in dataset_categories:
            coco_data["categories"].append({"id": category.id, "name": category.name, "supercategory": "none"})

        annotation_id_counter = 1
        for task in completed_tasks:
            file_name = task.image_path.split("/")[-1]

            coco_data["images"].append(
                {"id": task.task_id, "file_name": file_name, "width": task.width, "height": task.height}
            )

            for shape in task.shapes:
                coco_data["annotations"].append(
                    {
                        "id": annotation_id_counter,
                        "image_id": task.task_id,
                        "category_id": shape.get("category_id"),
                        "bbox": shape.get("bbox"),
                        "segmentation": shape.get("points"),
                        "iscrowd": shape.get("iscrowd"),
                    }
                )
                annotation_id_counter += 1

        return json.dumps(coco_data, ensure_ascii=False, indent=4)
