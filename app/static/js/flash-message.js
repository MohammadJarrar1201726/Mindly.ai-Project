// Mapping object
const flashMessagesTypes = {
  success: "success",
  error: "error",
  warning: "warning",
  info: "info",
};

// Object containing details for different types of toasts
const flashMessageDetails = {
  timer: 5000,
  success: {
    icon: "fa-circle-check",
  },
  error: {
    icon: "fa-circle-xmark",
  },
  warning: {
    icon: "fa-triangle-exclamation",
  },
  info: {
    icon: "fa-circle-info",
  },
};

const removeFlashMessage = (flashMessage) => {
  flashMessage.classList.add("hide");

  if (flashMessage.timeoutId) clearTimeout(flashMessage.timeoutId);

  setTimeout(() => flashMessage.remove(), 500); // Removing the toast after 500ms
};

const createFlashMessage = (type, text) => {
  let notifications = document.getElementById("flash-messages-container");

  // Getting the icon and text for the toast based on the id passed
  let { icon } = flashMessageDetails[type];
  let flashMessage = document.createElement("li");
  flashMessage.className = `flash-message ${type}`;

  flashMessage.innerHTML = `<div class="column">
                                <i class="fa-solid ${icon}"></i>
                                <span>${text}</span>
                                </div>
                                <i class="fa-solid fa-xmark" onclick="removeFlashMessage(this.parentElement)"></i>`;

  notifications.appendChild(flashMessage);

  // Setting a timeout to remove the flashMessage after the specified duration
  flashMessage.timeoutId = setTimeout(
    () => removeFlashMessage(flashMessage),
    flashMessageDetails.timer
  );
};
