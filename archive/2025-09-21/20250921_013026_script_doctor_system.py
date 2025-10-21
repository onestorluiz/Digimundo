from scripturemon_champion.script_doctor import analyze_script as analyze_script_minimal
class ScriptDoctorMinimal:
    def analyze_script(self, text: str):
        return analyze_script_minimal(text).to_dict()
