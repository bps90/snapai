import { Field } from "@/lib/fetchers"
import TextField, { TextField as TextFieldType } from "./TextField"
import { HTMLAttributes } from "react"
import { Control, UseFormRegister } from "react-hook-form"
import { ConfigFormSchema } from "../ConfigForm"
import NumberField, { NumberField as NumberFieldType } from "./NumberField"
import CheckboxField, { CheckboxField as CheckboxFieldType } from "./CheckboxField"
import NumberPairField, { NumberPairField as NumberPairFieldType } from "./NumberPairField"
import ModelSelectField, { ModelSelectField as ModelSelectFieldType } from "./ModelSelectField"
import PercentageField, { PercentageField as PercentageFieldType } from "./PercentageField"
import SelectField, { SelectField as SelectFieldType } from "./SelectField"
import MultiSelectField, { MultiSelectField as MultiSelectFieldType } from "./MultiSelectField"

export type FormFieldProps = {
    field: Field
    fieldIndex: number;
    containerAttr?: HTMLAttributes<HTMLDivElement>;
    register: UseFormRegister<ConfigFormSchema>;
    control: Control<ConfigFormSchema>;
    disabled?: boolean;
    nestedPaths?: string[]
    [key: string]: unknown
}

export default function FormField({
    field,
    disabled,
    ...fieldAttrs
}: FormFieldProps) {
    switch (field.type) {
        case 'text':
            return <TextField field={field as TextFieldType} inputAttr={{ disabled }} {...fieldAttrs} />
        case 'number':
            return <NumberField field={field as NumberFieldType} inputAttr={{ disabled }} {...fieldAttrs} />
        case 'checkbox':
            return <CheckboxField field={field as CheckboxFieldType} checkboxAttr={{ disabled }} {...fieldAttrs} />
        case 'number_pair':
            return <NumberPairField field={field as NumberPairFieldType} inputsAttr={{ disabled }} {...fieldAttrs} />
        case 'model_select':
            return <ModelSelectField field={field as ModelSelectFieldType} selectAttr={{ disabled }} {...fieldAttrs} />
        case 'percentage':
            return <PercentageField field={field as PercentageFieldType} inputAttr={{ disabled }} {...fieldAttrs} />
        case 'select':
            return <SelectField field={field as SelectFieldType} selectAttr={{ disabled }} {...fieldAttrs} />
        case 'multiselect':
            return <MultiSelectField field={field as MultiSelectFieldType} selectAttr={{ disabled }} {...fieldAttrs} />
        default:
            return null;
    }
}