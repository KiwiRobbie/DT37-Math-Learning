import json

# Class for updating save file and holding various data
class SaveManager:
    # Load json data and module / section keys
    def __init__(self, json_save, json_section, module, section):
        self.json_save, self.json_section, self.module, self.section = \
            json_save, json_section, module, section

    # Update a key for the current section by writing a new value or offsetting an existing one
    def update_key(self, key, value=None, offset=None):
        if type(value) is int:
            self.json_save[self.module][self.section][key] = value
        else:
            self.json_save[self.module][self.section][key] += offset

    # Use the current save data to update the progress key for the current section
    def update_progress(self):
        total = sum(list(self.json_section["Queue"].values()))
        progress = sum([self.json_save[self.module][self.section][key] for key in self.json_section["Queue"].keys()])
        self.json_save[self.module][self.section]["Progress"] = (total - progress) / total

    # Write the save data to a save.json file
    def update_save(self):
        # Update the progress for the section before writing
        self.update_progress()
        with open("data/save.json", "w") as f:
            # Return to the start of the file
            f.seek(0)

            # Dump json data
            json.dump(self.json_save, f, indent=4)

            # Remove any data after current location in file
            f.truncate()
