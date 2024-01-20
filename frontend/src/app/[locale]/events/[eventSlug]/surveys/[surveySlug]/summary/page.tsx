import { notFound } from "next/navigation";
import FieldSummaryComponent from "./FieldSummaryComponent";
import { ReturnLink } from "./ReturnLink";
import { gql } from "@/__generated__";
import { getClient } from "@/apolloClient";
import { auth } from "@/auth";
import { DimensionFilters } from "@/components/dimensions/DimensionFilters";
import { buildDimensionFilters } from "@/components/dimensions/helpers";
import {
  Layout,
  validateFields,
  validateSummary,
} from "@/components/SchemaForm/models";
import SchemaFormField from "@/components/SchemaForm/SchemaFormField";
import SignInRequired from "@/components/SignInRequired";
import ViewContainer from "@/components/ViewContainer";
import ViewHeading from "@/components/ViewHeading";
import getPageTitle from "@/helpers/getPageTitle";
import { getTranslations } from "@/translations";

const query = gql(`
  query SurveySummary(
    $eventSlug: String!,
    $surveySlug: String!,
    $locale: String,
    $filters: [DimensionFilterInput!],
  ) {
    event(slug: $eventSlug) {
      name

      forms {
        survey(slug: $surveySlug) {
          title(lang: $locale)
          fields(lang: $locale)
          summary(filters: $filters)
          countFilteredResponses: countResponses(filters: $filters)
          countResponses
          dimensions {
            slug
            title(lang: $locale)
            values {
              slug
              title(lang: $locale)
            }
          }
        }
      }
    }
  }
`);

interface Props {
  params: {
    locale: string;
    eventSlug: string;
    surveySlug: string;
  };
  searchParams: {
    [key: string]: string;
  };
}

export async function generateMetadata({ params, searchParams }: Props) {
  const { locale, eventSlug, surveySlug } = params;
  const translations = getTranslations(locale);

  // TODO encap
  const session = await auth();
  if (!session) {
    return translations.SignInRequired.metadata;
  }

  const t = translations.Survey;

  const { from: _, ...filterSearchParams } = searchParams;
  const filters = buildDimensionFilters(filterSearchParams);
  const { data } = await getClient().query({
    query,
    variables: { eventSlug, surveySlug, locale, filters },
  });

  if (!data.event?.forms?.survey) {
    notFound();
  }

  const title = getPageTitle({
    translations,
    event: data.event,
    subject: data.event.forms.survey.title,
    viewTitle: t.summaryTitle,
  });

  return { title };
}

export default async function SummaryPage({ params, searchParams }: Props) {
  const { locale, eventSlug, surveySlug } = params;
  const translations = getTranslations(locale);
  const t = translations.Survey;
  const session = await auth();

  // TODO encap
  if (!session) {
    return <SignInRequired messages={translations.SignInRequired} />;
  }

  // TODO: Make "from" a reserved word in the form generator
  const { from: _, ...filterSearchParams } = searchParams;
  const filters = buildDimensionFilters(filterSearchParams);
  const { data } = await getClient().query({
    query,
    variables: { eventSlug, surveySlug, locale, filters },
  });

  if (!data.event?.forms?.survey?.summary) {
    notFound();
  }

  const survey = data.event.forms.survey;
  const fields = survey.fields || [];
  const summary = survey.summary;
  const dimensions = survey.dimensions || [];

  validateFields(fields);
  validateSummary(summary);

  return (
    <ViewContainer>
      <ReturnLink messages={t.actions} />
      <ViewHeading>
        {t.summaryTitle}
        <ViewHeading.Sub>{survey.title}</ViewHeading.Sub>
      </ViewHeading>
      <DimensionFilters dimensions={dimensions} />
      <p>{t.summaryOf(survey.countFilteredResponses, survey.countResponses)}</p>
      {fields.map((field) => (
        <SchemaFormField
          key={field.slug}
          field={field}
          layout={Layout.Vertical}
        >
          {summary[field.slug] && (
            <FieldSummaryComponent
              translations={translations}
              field={field}
              fieldSummary={summary[field.slug]}
            />
          )}
        </SchemaFormField>
      ))}
    </ViewContainer>
  );
}
