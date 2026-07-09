def show_experiment_summary(experiment_input):
    print()
    print("===================================")
    print("Experiment Input Summary")
    print("===================================")

    input_type = experiment_input["input_type"]

    if input_type == "system_description":
        print("Input Type       : System Description")
        print("System Loaded    : Yes")
        print("Components Loaded: No")
        print("Image Loaded     : No")

    elif input_type == "system_description_with_components":
        print("Input Type       : System Description + Component List")
        print("System Loaded    : Yes")
        print(f"Components Loaded: Yes ({len(experiment_input['component_list'])} components)")
        print("Image Loaded     : No")

    elif input_type == "image":
        print("Input Type       : Image / P&ID Diagram")
        print("System Loaded    : No")
        print("Components Loaded: No")
        print("Image Loaded     : Yes")
        print(f"Image Path       : {experiment_input['image_path']}")

    print("===================================")