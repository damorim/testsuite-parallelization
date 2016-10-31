import os

from support import maven


class ExecutionData:
    def __init__(self, subject="N/A"):
        self.subject = subject
        self.builder_name = "N/A"
        self.compiled = False
        self.tests_pass = False
        self.tests = 0
        self.skipped = 0
        self.elapsed_t = 0
        self.system_t = 0
        self.user_t = 0
        self.cpu_usage = 0

    def values(self):
        return [self.subject, self.builder_name, self.compiled, self.tests_pass, self.tests, self.skipped,
                self.elapsed_t, self.system_t, self.user_t, self.cpu_usage]

    @staticmethod
    def header():
        return ["subject", "builder_name", "compiled", "tests_pass", "tests", "skipped",
                "elapsed_t", "system_t", "user_t", "cpu_usage"]


# FIXME test this!
def compute_time_distribution(data):
    test_cases = sorted(data.items, key=lambda t: t.time)
    total_time = data.statistics['time']
    coverage = 0.9

    threshold = total_time * coverage
    counter = 0
    current_time = 0.0
    for tc in test_cases:
        current_time += tc.time
        counter += 1
        print(" ", threshold, current_time)
        if current_time >= threshold:
            break
    print(data.statistics, threshold, counter, current_time)


def main(subject_name, subjects_home=os.curdir):
    subject_dir = os.path.join(subjects_home, subject_name)
    if not os.path.exists(subject_dir):
        print("Missing path:", subject_dir)
        return

    output_data = ExecutionData(subject_name)

    os.chdir(subject_dir)
    if maven.is_maven_project():
        output_data.builder_name = "Maven"
        if maven.build():
            output_data.compiled = True
            output_data.tests_pass = maven.test(output_data)

            test_data = maven.collect_surefire_data()
            compute_time_distribution(test_data)

    return output_data

if __name__ == "__main__":
    os.chdir("./subjects/storm")
    compute_time_distribution(maven.collect_surefire_data())
