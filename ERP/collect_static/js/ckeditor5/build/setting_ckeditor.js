function getcsrftoken() {
  var name = "csrftoken";
  var cookieValue = null;
  if (document.cookie && document.cookie != "") {
    var cookies = document.cookie.split(";");
    for (var i = 0; i < cookies.length; i++) {
      var cookie = cookies[i].trim();
      if (cookie.substring(0, name.length + 1) == name + "=") {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}

class MyUploadAdapter {
  constructor(loader) {
    this.loader = loader;
  }

  upload() {
    return this.loader.file.then(
      (file) =>
        new Promise((resolve, reject) => {
          this._initRequest();
          this._initListeners(resolve, reject, file);
          this._sendRequest(file);
        })
    );
  }

  _initRequest() {
    const xhr = (this.xhr = new XMLHttpRequest());

    xhr.open("POST", "/restful/saveimg", true);
    xhr.setRequestHeader("Authorization", "Bearer " + getcsrftoken());
    xhr.setRequestHeader("X-CSRFToken", getcsrftoken());
    xhr.responseType = "json";
  }

  _initListeners(resolve, reject, file) {
    const xhr = this.xhr;
    const loader = this.loader;
    const genericErrorText = `Couldn't upload file: ${file.name}.`;

    xhr.addEventListener("error", () => reject(genericErrorText));
    xhr.addEventListener("abort", () => reject());
    xhr.addEventListener("load", () => {
      const response = xhr.response;

      if (!response || response.error) {
        return reject(
          response && response.error ? response.error.message : genericErrorText
        );
      }

      resolve({
        default: response.url,
      });
    });

    if (xhr.upload) {
      xhr.upload.addEventListener("progress", (evt) => {
        if (evt.lengthComputable) {
          loader.uploadTotal = evt.total;
          loader.uploaded = evt.loaded;
        }
      });
    }
  }

  _sendRequest(file) {
    const data = new FormData();

    data.append("upload_img", file);
    data.append("X-CSRFToken", getcsrftoken());

    this.xhr.send(data);
  }

  abort() {
    if (this.xhr) {
      this.xhr.abort();
    }
  }
}

function MyCustomUploadAdapterPlugin(editor) {
  editor.plugins.get("FileRepository").createUploadAdapter = (loader) => {
    return new MyUploadAdapter(loader);
  };
}

ClassicEditor.create(document.querySelector("#ckeditor5"), {
  toolbar: {},
  extraPlugins: [MyCustomUploadAdapterPlugin],
  // "name": "content",
  link: {
    addTargetToExternalLinks: true,
  },
  fontColor: {
    colors: [
      {
        color: "hsl(0, 0%, 50%)",
        label: "Grey",
      },
      {
        color: "hsl(60, 100%, 50%)",
        label: "Yellow",
      },
      {
        color: "hsl(120, 100%, 50%)",
        label: "Green",
      },
      {
        color: "hsl(180, 100%, 50%)",
        label: "Cyan",
      },
      {
        color: "hsl(240, 100%, 50%)",
        label: "Blue",
      },
      {
        color: "hsl(300, 100%, 50%)",
        label: "Magenta",
      },
      {
        color: "hsl(0, 100%, 50%)",
        label: "Red",
      },
      {
        color: "hsl(300, 50%, 50%)",
        label: "Pink",
      },
      {
        color: "hsl(30, 100%, 50%)",
        label: "Orange",
      },
    ],
  },
  fontBackgroundColor: {
    colors: [
      {
        color: "hsl(0, 0%, 50%)",
        label: "Grey",
      },
      {
        color: "hsl(60, 100%, 50%)",
        label: "Yellow",
      },
      {
        color: "hsl(120, 100%, 50%)",
        label: "Green",
      },
      {
        color: "hsl(180, 100%, 50%)",
        label: "Cyan",
      },
      {
        color: "hsl(240, 100%, 50%)",
        label: "Blue",
      },
      {
        color: "hsl(300, 100%, 50%)",
        label: "Magenta",
      },
      {
        color: "hsl(0, 100%, 50%)",
        label: "Red",
      },
      {
        color: "hsl(300, 50%, 50%)",
        label: "Pink",
      },
      {
        color: "hsl(30, 100%, 50%)",
        label: "Orange",
      },
    ],
  },
})
  .then((editor) => {
    editor.model.document.on("change:data", () => {
      let htmlData = editor.getData({ exportData: "html" });
    });
    window.editor = editor;

    // editor.setData("ee");
    // console.log(editor);
  })
  .catch((error) => {
    console.error(error);
  });
