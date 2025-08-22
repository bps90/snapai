import { CheckboxField } from "@/components/form/fields/CheckboxField";
import { ModelSelectField } from "@/components/form/fields/ModelSelectField";
import { MultiSelectField } from "@/components/form/fields/MultiSelectField";
import { NodeSelectField } from "@/components/form/fields/NodeSelectField";
import { NumberField } from "@/components/form/fields/NumberField";
import { NumberPairField } from "@/components/form/fields/NumberPairField";
import { TextField } from "@/components/form/fields/TextField";
import { FieldType, Layout, Section } from "@/lib/fetchers";
import { z } from "zod";

export type LayoutWithNestedPaths = Layout & { nestedPaths?: string[] };
export type BuildSchemaLayout = {
    sections: {
        subsections: {
            lines: {
                fields: {
                    type: FieldType,
                    name: string,
                    nested_paths: string[]
                }[]
            }[]
        }[]
    }[]
    nestedPaths?: string[]
};

export type GetLayoutValuesLayout = {
    sections: {
        subsections: {
            lines: {
                fields: {
                    type: FieldType,
                    name: string,
                    value: unknown,
                    nested_paths: string[]
                }[]
            }[]
        }[]
    }[];
    nestedPaths?: string[]
}

export class FormLayoutHelper {
    public static buildSchema<ReturnedSchema extends z.ZodObject<any>>(
        layouts: BuildSchemaLayout[],
        defaultSchema: Record<string, z.ZodType> = {}
    ): ReturnedSchema {
        const schema: Record<string, z.ZodType> = defaultSchema;

        for (const layout of layouts) {
            for (const section of layout.sections) {
                for (const subsection of section.subsections) {
                    for (const line of subsection.lines) {
                        for (const field of line.fields) {
                            let base: z.ZodType;

                            switch (field.type) {
                                case 'text':
                                    base = z.string().min((field as TextField).min_length).max((field as TextField).max_length || Infinity);
                                    break;
                                case 'number':
                                    base = ((field as NumberField).is_float ? z.number() : z.number().int()).min((field as NumberField).min_value || -Infinity).max((field as NumberField).max_value || Infinity);
                                    break;
                                case 'checkbox':
                                    base = (field as CheckboxField).required ? z.literal(true) : z.preprocess((value) => Boolean(value), z.boolean());
                                    break;
                                case 'number_pair':
                                    base = z.tuple([
                                        ((field as NumberPairField).is_float ? z.number() : z.number().int()).min((field as NumberPairField).min_left_value || -Infinity).max((field as NumberPairField).max_left_value || Infinity),
                                        ((field as NumberPairField).is_float ? z.number() : z.number().int()).min((field as NumberPairField).min_right_value || -Infinity).max((field as NumberPairField).max_right_value || Infinity),
                                    ]).refine(([left, right]) => (field as NumberPairField).right_should_be_gte_left ? left <= right : true, { message: 'Right value should be greater than or equal to left value' });
                                    break;
                                case 'select':
                                    base = z.any();
                                    break;
                                case 'multiselect':
                                    base = z.array(z.any()).min((field as MultiSelectField).min_selected).max((field as MultiSelectField).max_selected || Infinity);
                                    break;
                                case 'percentage':
                                    base = z.number().max(100).min(0);
                                    break
                                case 'model_select':
                                    base = (field as ModelSelectField).required ? z.string().min(1, "Model name is required!") : z.string();
                                    break
                                case 'node_select':
                                    base = (field as NodeSelectField).required ? z.string().min(1, "Node name is required!") : z.string();
                                    break
                                case 'color':
                                    base = z.string().length(7).startsWith('#')
                                        .or(z.string().length(9).startsWith('#'));
                                    break
                                default:
                                    throw new Error(`Unknown field type: ${field.type}`);
                            }

                            const nestedPaths = layout.nestedPaths
                                ? [...layout.nestedPaths, ...field.nested_paths]
                                : field.nested_paths;

                            if (nestedPaths.length) {
                                const nestedSchema = FormLayoutHelper.buildSchema([{
                                    sections: [{
                                        subsections: [{
                                            lines: [{ fields: [{ ...field, nested_paths: nestedPaths.slice(1) }] }]
                                        }]
                                    }]
                                }], schema[nestedPaths[0]] ? { ...(schema[nestedPaths[0]] as z.ZodObject<any>).shape } : {});

                                schema[nestedPaths[0]] = schema[nestedPaths[0]]
                                    ? (schema[nestedPaths[0]] as z.ZodObject<any>).merge(nestedSchema)
                                    : nestedSchema;
                            } else {
                                schema[field.name] = base;
                            }

                        }
                    }
                }
            }
        }

        return z.object(schema) as ReturnedSchema;
    }

    public static getLayoutValues(layouts: GetLayoutValuesLayout[]) {
        const values = {} as Record<string, any>;

        for (const layout of layouts) {
            for (const section of layout.sections) {
                for (const subsection of section.subsections) {
                    for (const line of subsection.lines) {
                        for (const field of line.fields) {
                            const nestedPaths = layout.nestedPaths
                                ? [...layout.nestedPaths, ...field.nested_paths]
                                : field.nested_paths;

                            if (nestedPaths.length) {

                                const nestedValues = FormLayoutHelper.getLayoutValues([{
                                    sections: [{
                                        subsections: [{
                                            lines: [{ fields: [{ ...field, nested_paths: nestedPaths.slice(1) }] }]
                                        }]
                                    }]
                                }]);

                                values[nestedPaths[0]] = values[nestedPaths[0]]
                                    ? { ...values[nestedPaths[0]], ...nestedValues }
                                    : nestedValues;
                            } else {
                                values[field.name] = field.value;
                            }
                        }
                    }
                }
            }
        }

        return values;
    }

    public static getModelNameFieldsPathsAndSections(layouts: LayoutWithNestedPaths[]) {
        const values: Record<string, Section> = {};

        for (const layout of layouts) {
            for (const section of layout.sections) {
                for (const subsection of section.subsections) {
                    for (const line of subsection.lines) {
                        for (const field of line.fields) {
                            if (field.type !== 'model_select') continue;

                            const nestedPaths = layout.nestedPaths
                                ? [...layout.nestedPaths, ...field.nested_paths, field.name]
                                : [...field.nested_paths, field.name];

                            values[nestedPaths.join('.')] = section;
                        }
                    }
                }
            }
        }

        return values;
    }
}
