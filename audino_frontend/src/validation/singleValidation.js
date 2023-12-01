import Validator from "validatorjs";
import { attributeRule, projectRule, taskAddRule, taskEditRule } from "./rule";

export const projectSingleFieldValidation = ({ key, value }) => {
  const validationResponse = { isValid: true };
  if (projectRule[key]) {
    const validation = new Validator(
      { [key]: value },
      { [key]: projectRule[key] }
    );
    validationResponse.isValid = validation.passes();
    if (!validationResponse.isValid) {
      validationResponse.errors = validation.errors.all();
    }
  }
  return validationResponse;
};

export const attributeSingleFieldValidation = ({ key, value }) => {
  const validationResponse = { isValid: true };
  if (attributeRule[key]) {
    const validation = new Validator(
      { [key]: value },
      { [key]: attributeRule[key] }
    );
    validationResponse.isValid = validation.passes();
    if (!validationResponse.isValid) {
      validationResponse.errors = validation.errors.all();
    }
  }
  return validationResponse;
};

export const taskAddSingleFieldValidation = ({ key, value }) => {
  const validationResponse = { isValid: true };
  if (taskAddRule[key]) {
    const validation = new Validator(
      { [key]: value },
      { [key]: taskAddRule[key] }
    );
    validationResponse.isValid = validation.passes();
    if (!validationResponse.isValid) {
      validationResponse.errors = validation.errors.all();
    }
  }
  return validationResponse;
};
export const taskEditSingleFieldValidation = ({ key, value }) => {
  const validationResponse = { isValid: true };
  if (taskEditRule[key]) {
    const validation = new Validator(
      { [key]: value },
      { [key]: taskEditRule[key] }
    );
    validationResponse.isValid = validation.passes();
    if (!validationResponse.isValid) {
      validationResponse.errors = validation.errors.all();
    }
  }
  return validationResponse;
};

export const organizationSingleFieldValidation = ({ key, value }) => {
  const validationResponse = { isValid: true };

  if (key.startsWith("contact.")) {
    const contactField = key.substring("contact.".length);
    if (attributeRule.contact && attributeRule.contact[contactField]) {
      const validation = new Validator(
        { contact: { [contactField]: value } },
        { contact: { [contactField]: attributeRule.contact[contactField] } }
      );
      validationResponse.isValid = validation.passes();
      if (!validationResponse.isValid) {
        validationResponse.errors = {
          contact: {
            [contactField]: validation.errors.first(`contact.${contactField}`),
          },
        };
      }
    }
  } else if (attributeRule[key]) {
    const validation = new Validator(
      { [key]: value },
      { [key]: attributeRule[key] }
    );
    validationResponse.isValid = validation.passes();
    if (!validationResponse.isValid) {
      validationResponse.errors = { [key]: validation.errors.first(key) };
    }
  }

  return validationResponse;
};
