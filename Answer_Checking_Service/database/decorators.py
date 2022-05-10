def singleton(class_name):
    instances = {}

    def get_instance():
        if class_name not in instances:
            instances[class_name] = class_name()
        return instances[class_name]

    return get_instance

