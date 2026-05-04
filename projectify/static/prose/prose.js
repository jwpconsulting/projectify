/*! SPDX-License-Identifier: MIT
    SPDX-FileCopyrightText: 2022 LOGIC SMPC <paris@withlogic.co> */
// This code goes in /static/prose/editor.js or similar
async function uploadFile(host, attachment) {
  const csrfToken = document.querySelector(
    "input[name=csrfmiddlewaretoken]",
  ).value;

  const { file } = attachment;
  const formData = new FormData();
  formData.append("file", file);
  formData.append("Content-Type", file.type);
  formData.append("csrfmiddlewaretoken", csrfToken);

  // This used to support progress updating before
  const response = await fetch(host, { method: "POST", body: formData });
  if (response.status !== 201) {
    throw new Error(`Bad response ${response.status}`);
  }
  const data = await response.json();
  const result = { url: data.url, href: data.url };
  attachment.setAttributes(result);
}

/**
 * https://github.com/withlogicco/django-prose/issues/100
 */
function patchTrixEditorWithNameSetter() {
  Object.defineProperty(
    window.Trix.elements.TrixEditorElement.prototype,
    "name",
    {
      get() {
        return this.inputElement?.name;
      },
      set(value) {
        this.inputElement.name = value;
      },
    },
  );
}

// When the DOM is initially loaded
document.addEventListener("DOMContentLoaded", () => {
  patchTrixEditorWithNameSetter();
  document.addEventListener("trix-before-initialize", configureToolbar);
  // https://github.com/basecamp/trix/issues/117#issuecomment-463275725
  // https://github.com/basecamp/trix/issues/680#issuecomment-735742942
  Trix.config.blockAttributes.default.tagName = "p";
  Trix.config.blockAttributes.default.breakOnReturn = true;

  Trix.Block.prototype.breaksOnReturn = function () {
    const attr = this.getLastAttribute();
    // https://github.com/basecamp/trix/issues/680#issuecomment-1591104806
    const config = Trix.config.blockAttributes[attr ? attr : "default"];
    return config ? config.breakOnReturn : false;
  };
  Trix.LineBreakInsertion.prototype.shouldInsertBlockBreak = function () {
    if (
      this.block.hasAttributes() &&
      this.block.isListItem() &&
      !this.block.isEmpty()
    ) {
      return this.startLocation.offset > 0;
    } else {
      return !this.shouldBreakFormattedBlock() ? this.breaksOnReturn : false;
    }
  };
});

function initializeLinkSuggestions(editor, suggestLinksUrl) {
  const dialog = document.getElementById("prose-link-suggestions-dialog");
  if (dialog === null) {
    throw new Error("Couldn't find link suggestions dialog");
  }

  async function showWidget(trixEditor) {
    const selectedRange = trixEditor.getSelectedRange();
    const selectedText = selectedRange[0] !== selectedRange[1];
    const searchString = selectedText
      ? `?search=${trixEditor.getDocument().toString().slice(selectedRange[0], selectedRange[1])}`
      : "";

    await htmx.ajax("GET", `${suggestLinksUrl}${searchString}`, {
      target: dialog,
      swap: "innerHTML",
    });

    dialog.showModal();

    const closeButton = dialog.querySelector('[name="close"]');
    if (closeButton === null) {
      throw new Error("Couldn't find close button");
    }
    closeButton.addEventListener("click", dialog.close);

    // Find list of results inside dialog. The results hold url and
    // title data- attributes
    const results = document.getElementById("prose-link-suggestions-results");
    if (results === null) {
      throw new Error("Couldn't find #prose-link-suggestions-results");
    }
    results.addEventListener("click", (event) => {
      if (!event.target.dataset.url) {
        console.error(
          "Received click event for a button with no data-url set",
        );
        return;
      }

      const { url, title } = event.target.dataset;
      const [start, end] = trixEditor.getSelectedRange();
      const textSelected = start !== end;
      if (textSelected) {
        // Potential sink for XSS
        // Trix relies on DOMPurify
        trixEditor.activateAttribute("href", url);
      } else {
        const start = trixEditor.getPosition();
        trixEditor.insertString(title);
        const end = trixEditor.getPosition();
        trixEditor.setSelectedRange([start, end]);
        trixEditor.activateAttribute("href", url);
        trixEditor.setSelectedRange([end, end]);
      }
      dialog.close();
    });
  }

  editor.addEventListener("trix-action-invoke", (event) => {
    if (event.actionName !== "x-suggest-links") {
      return;
    }
    // Already open
    if (dialog.open) {
      return;
    }
    const { editor: trixEditor } = event.target;
    showWidget(trixEditor);
  });
}
/*! SPDX-SnippetBegin
   SPDX-License-Identifier: MIT
   SPDX-SnippetCopyrightText: 2022 beta.gouv.fr
   Source:
   https://github.com/betagouv/complements-alimentaires/blob/95b70bafdf4f4a86914711507270dc8079e42df9/data/static/extend-buttons.js */
function createTrixButton(text, title) {
  const button = document.createElement("button");
  button.type = "button";
  button.className = "trix-button";
  button.title = title;
  button.textContent = text;
  return button;
}
// See "Toggle Attribute" in Trix documentation
function createAttributeButton(text, title, attribute) {
  const button = createTrixButton(text, title);
  button.setAttribute("data-trix-attribute", attribute);
  return button;
}
// See "Invoking Internal Trix Actions" in Trix documentation
function createActionButton(text, title, action) {
  const button = createTrixButton(text, title);
  button.setAttribute("data-trix-action", action);
  return button;
}

function configureToolbar(event) {
  const editor = event.target;
  const { toolbarElement } = editor;

  if (editor.dataset.headingBlocks === "True") {
    Trix.config.blockAttributes.subHeadingh2 = { tagName: "h2" };
    Trix.config.blockAttributes.subHeadingh3 = { tagName: "h3" };

    const trixTitleButton = toolbarElement.querySelector(
      "[data-trix-attribute=heading1]",
    );
    const h2Button = createAttributeButton(
      "H2",
      "Subheading H2",
      "subHeadingh2",
    );
    trixTitleButton.insertAdjacentElement("afterend", h2Button);

    const h3Button = createAttributeButton(
      "H3",
      "Subheading H3",
      "subHeadingh3",
    );
    h2Button.insertAdjacentElement("afterend", h3Button);
  }

  const uploadUrl = editor.dataset.uploadAttachmentUrl;
  if (uploadUrl) {
    editor.addEventListener("trix-attachment-add", (event) =>
      uploadFile(uploadUrl, event.attachment),
    );
  } else {
    editor.addEventListener("trix-file-accept", function (event) {
      event.preventDefault();
    });
    const fileToolsGroup = toolbarElement.querySelector(
      ".trix-button-group--file-tools",
    );
    if (!fileToolsGroup) {
      throw new Error("Couldn't find file-tools");
    }
    fileToolsGroup.remove();
  }
  // Only initialize the link suggester if the editor has a
  // data-suggest-links-url property
  if (editor.dataset.suggestLinksUrl) {
    const buttonGroup = toolbarElement.querySelector(
      ".trix-button-group--text-tools",
    );
    if (buttonGroup === null) {
      throw new Error("Couldn't find Trix button group");
    }
    const suggestLinksButton = createActionButton(
      "Project/Task",
      "Suggest links",
      "x-suggest-links",
    );
    buttonGroup.appendChild(suggestLinksButton);
    initializeLinkSuggestions(editor, editor.dataset.suggestLinksUrl);
  }
  editor.classList.add("initialized");
}
/*! SPDX-SnippetEnd */
