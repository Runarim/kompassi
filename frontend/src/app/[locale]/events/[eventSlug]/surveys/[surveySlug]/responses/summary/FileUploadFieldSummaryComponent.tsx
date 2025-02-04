import { FileUploadFieldSummary } from "@/components/SchemaForm/models";
import UploadedFileCards from "@/components/SchemaForm/UploadedFileCards";
import { Translations } from "@/translations/en";

interface Props {
  fieldSummary: FileUploadFieldSummary;
  translations: Translations;
}

export default function FileUploadFieldSummaryComponent({
  fieldSummary,
  translations,
}: Props) {
  const t = translations.Survey;
  const { summary, countResponses, countMissingResponses } = fieldSummary;
  return (
    <>
      <UploadedFileCards urls={summary} messages={translations.SchemaForm} />
      <p className="text-muted">
        {t.attributes.countResponses}: {countResponses}.{" "}
        {t.attributes.countMissingResponses}: {countMissingResponses}.
      </p>
    </>
  );
}
