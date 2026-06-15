from django.core.management.base import BaseCommand

from app.db.models.skill import Skill


DEFAULT_SKILLS = [
    "Python",
    "JavaScript",
    "Machine Learning",
    "Data Science",
    "Computer Vision",
    "NLP",
    "Web Development",
    "Mobile Development",
    "DevOps",
    "SQL",
    "Git",
    "Docker",
    "AWS",
    "React",
    "Node.js",
    "Java",
    "C++",
    "R",
    "TensorFlow",
    "PyTorch",
]


class Command(BaseCommand):
    help = "Initialize default skills"

    def handle(self, *args, **options):
        created_count = 0
        for skill_name in DEFAULT_SKILLS:
            _, created = Skill.objects.get_or_create(name=skill_name)
            if created:
                created_count += 1
                self.stdout.write(f"Created skill: {skill_name}")

        if created_count == 0:
            self.stdout.write("All skills already exist")
        else:
            self.stdout.write(f"Successfully created {created_count} skills")
