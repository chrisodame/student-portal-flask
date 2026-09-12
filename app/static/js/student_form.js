document.addEventListener("DOMContentLoaded", function () {

    const levelSelect = document.getElementById("level");
    const courseSelect = document.getElementById("course");

    if (!levelSelect || !courseSelect) {
        return;
    }

    function loadCourses(level) {

        courseSelect.innerHTML = "";

        if (!level) {
            const option = document.createElement("option");
            option.value = "";
            option.textContent = "Select a course";
            courseSelect.appendChild(option);
            return;
        }

        const loadingOption = document.createElement("option");
        loadingOption.value = "";
        loadingOption.textContent = "Loading courses...";
        courseSelect.appendChild(loadingOption);

        fetch(`/api/courses/${level}`)
            .then(response => {
                if (!response.ok) {
                    throw new Error("Unable to load courses.");
                }

                return response.json();
            })
            .then(data => {

                courseSelect.innerHTML = "";

                const defaultOption = document.createElement("option");
                defaultOption.value = "";
                defaultOption.textContent = "Select a course";
                courseSelect.appendChild(defaultOption);

                data.courses.forEach(function (course) {

                    const option = document.createElement("option");

                    option.value = course;
                    option.textContent = course;

                    courseSelect.appendChild(option);
                });

            })
            .catch(error => {

                console.error("Error loading courses:", error);

                courseSelect.innerHTML = "";

                const errorOption = document.createElement("option");
                errorOption.value = "";
                errorOption.textContent = "Unable to load courses";

                courseSelect.appendChild(errorOption);
            });
    }

    levelSelect.addEventListener("change", function () {
        loadCourses(this.value);
    });

    // Load courses automatically if a level is already selected
    if (levelSelect.value) {
        loadCourses(levelSelect.value);
    }

});