const translations = {
  AccommodationOnboardingView: {
    title: 'Accommodation onboarding',
  },
  Common: {
    ok: 'OK',
    cancel: 'Cancel',
    submit: 'Submit',
    search: 'Search',
  },
  DataTable: {
    create: 'Create',
  },
  Event: {
    title: 'Events',
    headline: 'Date and venue',
    name: 'Name',
    workInProgress: 'Kompassi v2 is a work in progress. This is not the final front page, but rather a demo of the table component.',
  },
  Navigation: {
    forms: 'Forms',
    logIn: 'Log in',
    logOut: 'Log out',
  },
  NotFound: {
    notFoundHeader: 'Page not found',
    notFoundMessage: 'The address does not conform to any of the recognized address patterns. Please double-check the address.',
  },
  SchemaForm: {
    submit: 'Submit',
  },
  Forms: {
    heading: 'Forms',
    title: 'Title',
    slug: 'Slug',
    create: 'New form',
  },
  MainView: {
    defaultErrorMessage: 'Something went wrong. There may be further information in the JavaScript console.',
  },
  FormEditor: {
    editField: 'Edit field',
    moveUp: 'Move up',
    moveDown: 'Move down',
    removeField: 'Remove field',
    addFieldAbove: 'Add field above',
    addField: 'Add field',
    save: 'Save form',
    cancel: 'Return without saving',
    saveFailedErrorMessage: 'Something went wrong while saving the form. There may be further information in the JavaScript console.',

    Tabs: {
      design: 'Design',
      preview: 'Preview',
      properties: 'Properties',
    },

    FormPropertiesForm: {
      title: {
        title: 'Form title',
        helpText: 'Human-readable form title. May not be displayed in all contexts.',
      },
      slug: {
        title: 'Technical name',
        helpText:
          'Machine-readable form name. Will be a part of the URL of the form. Valid characters: letters A-Za-z, numbers 0-9, underscore _. Must not start with a number.',
      },
      layout: {
        title: 'Layout',
        helpText: 'May not take effect in some contexts (eg. space-constrained forms may be forced to be horizontal).',
        choices: {
          horizontal: 'Horizontal',
          vertical: 'Vertical',
        },
      },
    },

    EditFieldForm: {
      name: {
        title: 'Technical name',
        helpText:
          'Machine-readable field name. Valid characters: letters A-Za-z, numbers 0-9, underscore _. Must not start with a number.',
      },
      title: {
        title: 'Title',
        helpText: 'Human-readable field label. If unset, defaults to field name.',
      },
      helpText: {
        title: 'Help text',
        helpText: 'Displayed below the field.',
      },
    },

    FieldTypes: {
      SingleLineText: 'Single line text field',
      MultiLineText: 'Multi-line text field',
      Divider: 'Divider',
      StaticText: 'Static text',
      Spacer: 'Empty space',
      SingleCheckbox: 'Single check box',
    },

    RemoveFieldModal: {
      title: 'Confirm field removal',
      message: 'Remove the selected field?',
      yes: 'Yes, remove',
      no: 'No, cancel',
    },
  },
};

export default translations;
