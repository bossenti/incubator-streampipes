package org.apache.streampipes.processors.changedetection.jvm.cumsum;

import org.apache.streampipes.commons.exceptions.SpRuntimeException;
import org.apache.streampipes.model.DataProcessorType;
import org.apache.streampipes.model.graph.DataProcessorDescription;
import org.apache.streampipes.model.runtime.Event;
import org.apache.streampipes.model.schema.PropertyScope;
import org.apache.streampipes.sdk.builder.ProcessingElementBuilder;
import org.apache.streampipes.sdk.builder.StreamRequirementsBuilder;
import org.apache.streampipes.sdk.helpers.*;
import org.apache.streampipes.sdk.utils.Assets;
import org.apache.streampipes.vocabulary.SO;
import org.apache.streampipes.wrapper.context.EventProcessorRuntimeContext;
import org.apache.streampipes.wrapper.routing.SpOutputCollector;
import org.apache.streampipes.wrapper.standalone.ProcessorParams;
import org.apache.streampipes.wrapper.standalone.StreamPipesDataProcessor;

import java.util.Arrays;


public class CumSumProcessor extends StreamPipesDataProcessor {

    private enum CumSumEventFieldNames {
        VAL_LOW ("cumSumLow"),
        VAL_HIGH ("cumSumHigh"),
        DECISION_LOW ("changeDetectedLow"),
        DECISION_HIGH ("changeDetectionHigh");


        private final String eventFieldName;
        CumSumEventFieldNames(String eventFieldName) {
            this.eventFieldName = eventFieldName;
        }

        public String toString(){
            return this.eventFieldName;
        }
    }

    private static final String NUMBER_MAPPING = "number-mapping";
    private static final String PARAM_K = "param-k";
    private static final String PARAM_H = "param-h";

    private String selectedNumberMapping;
    private Double k;
    private Double h;
    private Double cumSumLow;
    private Double cumSumHigh;
    private WelfordAggregate welfordAggregate;

    @Override
    public DataProcessorDescription declareModel() {
        return ProcessingElementBuilder
                .create("org.apache.streampipes.processors.changedetection.jvm.cumsum")
                .category(DataProcessorType.VALUE_OBSERVER)
                .withAssets(Assets.DOCUMENTATION, Assets.ICON)
                .withLocales(Locales.EN)
                .requiredStream(
                        StreamRequirementsBuilder
                                .create()
                                .requiredPropertyWithUnaryMapping(
                                        EpRequirements.numberReq(),
                                        Labels.withId(NUMBER_MAPPING),
                                        PropertyScope.NONE
                                )
                                .build()
                )
                .requiredFloatParameter(Labels.withId(PARAM_K), 0.0f, 0.0f, 100.0f, 0.01f)
                .requiredFloatParameter(Labels.withId(PARAM_H), 0.0f, 0.0f, 100.0f, 0.01f)
                .outputStrategy(
                        OutputStrategies.append(
                                Arrays.asList(
                                        EpProperties.numberEp(Labels.empty(), CumSumEventFieldNames.VAL_LOW.toString(), SO.Number),
                                        EpProperties.numberEp(Labels.empty(), CumSumEventFieldNames.VAL_HIGH.toString(), SO.Number),
                                        EpProperties.numberEp(Labels.empty(), CumSumEventFieldNames.DECISION_LOW.toString(), SO.Boolean),
                                        EpProperties.numberEp(Labels.empty(), CumSumEventFieldNames.DECISION_HIGH.toString(), SO.Boolean)
                                )
                        )
                )
                .build();
    }

    @Override
    public void onInvocation(ProcessorParams parameters, SpOutputCollector spOutputCollector, EventProcessorRuntimeContext runtimeContext) throws SpRuntimeException {
        this.selectedNumberMapping = parameters.extractor().singleValueParameter(NUMBER_MAPPING, String.class);
        this.k = parameters.extractor().singleValueParameter(PARAM_K, Double.class);
        this.h = parameters.extractor().singleValueParameter(PARAM_H, Double.class);
        this.cumSumLow = 0.0;
        this.cumSumHigh = 0.0;
        this.welfordAggregate = new WelfordAggregate();
    }

    @Override
    public void onEvent(Event event, SpOutputCollector collector) throws SpRuntimeException {
        Double value = event.getFieldBySelector(this.selectedNumberMapping).getAsPrimitive().getAsDouble();
        this.welfordAggregate.update(value);
        Double normalizedValue = this.welfordAggregate.getZScoreNormalizedValue(value);
        this.updateStatistics(normalizedValue);

    }

    private void updateStatistics(Double normalizedValue) {
        if (normalizedValue.isNaN()) {
            return;
        }
        this.cumSumHigh = Math.max(0, this.cumSumHigh + normalizedValue - this.k);
        this.cumSumLow = Math.min(0, this.cumSumLow + normalizedValue + this.k);
    }

    @Override
    public void onDetach() throws SpRuntimeException {
        this.cumSumLow = 0.0;
        this.cumSumHigh = 0.0;
        this.welfordAggregate = new WelfordAggregate();
    }
}
