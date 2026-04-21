/*! SPDX-License-Identifier: MIT
    SPDX-FileCopyrightText: 2022 LOGIC SMPC <paris@withlogic.co> */
// This code goes in /static/prose/editor.js or similar
async function uploadFile(host, attachment) {
  const csrfToken = document.querySelector("input[name=csrfmiddlewaretoken]").value;

  const { file } = attachment;
  const formData = new FormData();
  formData.append("file", file);
  formData.append("Content-Type", file.type);
  formData.append("csrfmiddlewaretoken", csrfToken);

  // This used to support progress updating before
  const response = await fetch(host, {method: "POST", body: formData});
  if (response.status !== 201) {
    throw new Error(`Bad response ${response.status}`);
  }
  const data = await response.json();
  const result = { url: data.url, href: data.url };
  attachment.setAttributes(result);
}

function initializeEditors() {
  const editors = document.querySelectorAll(".django-prose-editor:not(.initialized)");

  editors.forEach((editor) => {
    const uploadUrl = editor.dataset.uploadAttachmentUrl;
    if (uploadUrl) {
      editor.addEventListener("trix-attachment-add", (event) =>
        uploadFile(uploadUrl, event.attachment)
      );
    } else {
      editor.addEventListener("trix-file-accept", function (event) {
        event.preventDefault();
      });
    }
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
  document.addEventListener("trix-before-initialize", configureToolbar);
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
function createHeadingButton(attribute, title, text) {
  const button = document.createElement("button")
  button.type = "button"
  button.className = "trix-button"
  button.setAttribute("data-trix-attribute", attribute)
  button.title = title
  button.textContent = text
  return button
}

function configureToolbar(event) {
  const { toolbarElement } = event.target

  if (event.target.dataset.headingBlocks === "True") {
    Trix.config.blockAttributes.subHeadingh2 = { tagName: "h2" }
    Trix.config.blockAttributes.subHeadingh3 = { tagName: "h3" }

    const trixTitleButton = toolbarElement.querySelector(
      "[data-trix-attribute=heading1]",
    )
    const h2Button = createHeadingButton("subHeadingh2", "Subheading H2", "H2")
    trixTitleButton.insertAdjacentElement("afterend", h2Button)

    const h3Button = createHeadingButton("subHeadingh3", "Subheading H3", "H3")
    h2Button.insertAdjacentElement("afterend", h3Button)
  }

  if (!event.target.dataset.uploadAttachmentUrl) {
    const fileToolsGroup = toolbarElement.querySelector(".trix-button-group--file-tools")
    if (fileToolsGroup) {
      fileToolsGroup.remove()
    }
  }
}
// SPDX-SnippetEnd
