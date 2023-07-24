

class MyUploadAdapter {
    constructor(loader) {
        this.loader = loader;
    }

    upload() {
        return this.loader.file
            .then(file => new Promise((resolve, reject) => {
                this._initRequest();
                this._initListeners(resolve, reject, file);
                this._sendRequest(file);
            }));
    }

    _initRequest() {
        const xhr = this.xhr = new XMLHttpRequest();

        xhr.open('POST', '/upload', true);
        xhr.setRequestHeader('Authorization', 'Bearer ' + "csrf_token()");
        xhr.setRequestHeader('X-CSRFToken', "csrf_token");
        xhr.responseType = 'json';
    }

    _initListeners(resolve, reject, file) {
        const xhr = this.xhr;
        const loader = this.loader;
        const genericErrorText = `Couldn't upload file: ${file.name}.`;

        xhr.addEventListener('error', () => reject(genericErrorText));
        xhr.addEventListener('abort', () => reject());
        xhr.addEventListener('load', () => {
            const response = xhr.response;

            if (!response || response.error) {
                return reject(response && response.error ? response.error.message : genericErrorText);
            }

            resolve({
                default: response.url
            });
        });

        if (xhr.upload) {
            xhr.upload.addEventListener('progress', evt => {
                if (evt.lengthComputable) {
                    loader.uploadTotal = evt.total;
                    loader.uploaded = evt.loaded;
                }
            });
        }
    }

    _sendRequest(file) {
        const data = new FormData();

        data.append('upload', file);
        data.append('X-CSRFToken', "csrf_token()");

        this.xhr.send(data);
    }

    abort() {
        if (this.xhr) {
            this.xhr.abort();
        }
    }
}

function MyCustomUploadAdapterPlugin(editor) {
    editor.plugins.get("FileRepository").createUploadAdapter = loader => {
        return new MyUploadAdapter(loader);
    };
}


ClassicEditor.create(document.querySelector('#text'), {
    extraPlugins: [MyCustomUploadAdapterPlugin],

    fontColor: {
        colors: [
            {
                color: 'hsl(0, 0%, 50%)',
                label: 'Grey'
            },
            {
                color: 'hsl(60, 100%, 50%)',
                label: 'Yellow'
            },
            {
                color: 'hsl(120, 100%, 50%)',
                label: 'Green'
            },
            {
                color: 'hsl(180, 100%, 50%)',
                label: 'Cyan'
            },
            {
                color: 'hsl(240, 100%, 50%)',
                label: 'Blue'
            },
            {
                color: 'hsl(300, 100%, 50%)',
                label: 'Magenta'
            },
            {
                color: 'hsl(0, 100%, 50%)',
                label: 'Red'
            },
            {
                color: 'hsl(300, 50%, 50%)',
                label: 'Pink'
            },
            {
                color: 'hsl(30, 100%, 50%)',
                label: 'Orange'
            }
        ]
    }, fontBackgroundColor: {
        colors: [
            {
                color: 'hsl(0, 0%, 50%)',
                label: 'Grey'
            },
            {
                color: 'hsl(60, 100%, 50%)',
                label: 'Yellow'
            },
            {
                color: 'hsl(120, 100%, 50%)',
                label: 'Green'
            },
            {
                color: 'hsl(180, 100%, 50%)',
                label: 'Cyan'
            },
            {
                color: 'hsl(240, 100%, 50%)',
                label: 'Blue'
            },
            {
                color: 'hsl(300, 100%, 50%)',
                label: 'Magenta'
            },
            {
                color: 'hsl(0, 100%, 50%)',
                label: 'Red'
            },
            {
                color: 'hsl(300, 50%, 50%)',
                label: 'Pink'
            },
            {
                color: 'hsl(30, 100%, 50%)',
                label: 'Orange'
            }
        ]
    },
})
    .then(editor => {

        editor.model.document.on('change:data', () => {
            let htmlData = editor.getData({ 'exportData': 'html' });
            console.log(htmlData);
            console.log(editor.getData());
        });

        // console.log(editor);
    })
    .catch(error => {
        console.error(error);
    });