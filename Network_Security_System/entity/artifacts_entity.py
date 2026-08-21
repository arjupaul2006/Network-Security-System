from dataclasses import dataclass

@dataclass
class DataIngestionArtifacts:
    trained_file_path: str
    tested_file_path: str