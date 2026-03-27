/* SPDX-License-Identifier: MIT */
/* SPDX-FileCopyrightText: 2022 LOGIC SMPC <paris@withlogic.co> */
// This code goes in /static/prose/editor.js or similar
function uploadAttachment(host, attachment) {
  uploadFile(host, attachment.file, setProgress, setAttributes);

  function setProgress(progress) {
    attachment.setUploadProgress(progress);
  }

  function setAttributes(attributes) {
    attachment.setAttributes(attributes);
  }
}

function uploadFile(host, file, progressCallback, successCallback) {
  const formData = createFormData(file);
  // TODO use fetch
  const xhr = new XMLHttpRequest();
  const csrfToken = document.querySelector("input[name=csrfmiddlewaretoken]").value;

  formData.append("csrfmiddlewaretoken", csrfToken);

  xhr.open("POST", host, true);

  xhr.upload.addEventListener("progress", function (event) {
    const progress = (event.loaded / event.total) * 100;
    progressCallback(progress);
  });

  xhr.addEventListener("load", function (event) {
    if (xhr.status == 201) {
      const data = JSON.parse(xhr.response);
      const attributes = {
        url: data.url,
        href: `${data.url}?content-disposition=attachment`,
      };
      successCallback(attributes);
    }
  });

  xhr.send(formData);
}

function createFormData(file) {
  const data = new FormData();
  data.append("file", file);
  data.append("Content-Type", file.type);
  return data;
}

function initializeEditors() {
  const editors = document.querySelectorAll(".django-prose-editor:not(.initialized)");

  editors.forEach((editor) => {
    editor.addEventListener("trix-attachment-add", function (event) {
      uploadAttachment(editor.dataset.uploadAttachmentUrl, event.attachment);
    });
    editor.classList.add("initialized");
  });
}

/**
 * https://github.com/withlogicco/django-prose/issues/100
 */
function patchTrixEditorWithNameSetter() {
  Object.defineProperty(window.Trix.elements.TrixEditorElement.prototype, "name", {
    get() {
      return this.inputElement?.name;
    },
    set(value) {
      this.inputElement.name = value;
    },
  });
}

// When the DOM is initially loaded
document.addEventListener("DOMContentLoaded", () => {
  initializeEditors();
  patchTrixEditorWithNameSetter();
  configureToolbar();
  // https://github.com/basecamp/trix/issues/117#issuecomment-463275725
  // https://github.com/basecamp/trix/issues/680#issuecomment-735742942
  Trix.config.blockAttributes.default.tagName = "p"
  Trix.config.blockAttributes.default.breakOnReturn = true;

  Trix.Block.prototype.breaksOnReturn = function(){
    const attr = this.getLastAttribute();
    // https://github.com/basecamp/trix/issues/680#issuecomment-1591104806
    const config = Trix.config.blockAttributes[attr ? attr : "default"];
    return config ? config.breakOnReturn : false;
  };
  Trix.LineBreakInsertion.prototype.shouldInsertBlockBreak = function(){
    if(this.block.hasAttributes() && this.block.isListItem() && !this.block.isEmpty()) {
      return this.startLocation.offset > 0
    } else {
      return !this.shouldBreakFormattedBlock() ? this.breaksOnReturn : false;
    }
  };
});

// Export the initializeEditors function so it can be called from other scripts
window.djangoProse = window.djangoProse || {};
window.djangoProse.initializeEditors = initializeEditors;

// SPDX-SnippetBegin
// SPDX-License-Identifier: MIT
// SPDX-SnippetCopyrightText: 2022 beta.gouv.fr
// Source:
// https://github.com/betagouv/complements-alimentaires/blob/95b70bafdf4f4a86914711507270dc8079e42df9/data/static/extend-buttons.js
function configureToolbar() {
  Trix.config.blockAttributes.subHeadingh2 = { tagName: "h2" }
  Trix.config.blockAttributes.subHeadingh3 = { tagName: "h3" }

  const h2ButtonHTML =
    '<button type="button" class="trix-button" data-trix-attribute="subHeadingh2" title="Subheading H2">H2</button>'
  const h3ButtonHTML =
    '<button type="button" class="trix-button" data-trix-attribute="subHeadingh3" title="Subheading H3">H3</button>'

  document.addEventListener("trix-before-initialize", (event) => {
    const { toolbarElement } = event.target

    const trixTitleButton = toolbarElement.querySelector(
      "[data-trix-attribute=heading1]",
    )
    trixTitleButton.insertAdjacentHTML("afterend", h2ButtonHTML)
    trixTitleButton.remove()

    const h2Button = toolbarElement.querySelector("[data-trix-attribute=subHeadingh2]")
    h2Button.insertAdjacentHTML("afterend", h3ButtonHTML)
  })
}
// SPDX-SnippetEnd
