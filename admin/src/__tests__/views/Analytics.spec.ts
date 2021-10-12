import { createLocalVue, shallowMount, Wrapper } from '@vue/test-utils';
import ElementUI from 'element-ui';
import Analytics from '@/views/Analytics.vue';

jest.mock('@/client/analytics');
const localVue = createLocalVue();
localVue.use(ElementUI);

describe('Analytics.vue', () => {
  let wrapper: Wrapper<any>;
  let comp: any;
  const $route = {
    params: {
      agentName: 'testAgentName',
    },
  };
  beforeEach(() => {
    wrapper = shallowMount(Analytics, {
      localVue,
      mocks: {
        $route,
      },
    });
    comp = wrapper.vm;
  });

  afterEach(() => {
    jest.clearAllMocks();
    jest.resetAllMocks();
    wrapper.destroy();
  });

  describe('Testing Mount lifecycle', () => {
    it('should initialize properties', async () => {
      const intentDataList = ['intent1', 'intent2', 'FALLBACK', 'intent3', 'intent4'];
      expect(comp.$data.intentDataList).toEqual(intentDataList);
      const allDateDataList = [
        '2021-08-01',
        '2021-08-02',
        '2021-08-03',
        '2021-08-04',
        '2021-08-05',
        '2021-08-06',
        '2021-08-07',
        '2021-08-08',
      ];
      expect(comp.$data.allDateDataList).toEqual(allDateDataList);
      const allTraficDataList = [4, 2, 4, 4, 4, 4, 8, 5];
      expect(comp.$data.allTrafficDataList).toEqual(allTraficDataList);
      const allUniqueUsersDataList = [3, 11, 3, 3, 3, 3, 3, 1];
      expect(comp.$data.allUniqueUsersDataList).toEqual(allUniqueUsersDataList);
      const allFallbackDataList = [3, 0, 3, 3, 3, 1, 3, 5];
      expect(comp.$data.allFallbackDataList).toEqual(allFallbackDataList);
    });
  });

  describe('Testing computed properties', () => {
    it('should calculate chartDataLineTraffic', async () => {
      // last 30 days
      const chartDataLineTrafficComputedProperty = (comp as any).chartDataLineTraffic;
      expect(chartDataLineTrafficComputedProperty.labels).toEqual(comp.$data.dateDataList);
      expect(chartDataLineTrafficComputedProperty.datasets[0].label).toEqual('Traffic');
      expect(chartDataLineTrafficComputedProperty.datasets[0].data).toEqual(comp.$data.trafficDataList);

      (comp as any).selectPeriod('Last 7 days'); // trigger last 7 days selection

      expect(comp.$data.dateDataList.length).toEqual(7);
      expect(comp.$data.trafficDataList.length).toEqual(7);
    });

    it('should calculate chartDataLineUniqueUsers', async () => {
      // last 30 days
      const chartDataLineUniqueUsersComputedProperty = (comp as any).chartDataLineUniqueUsers;
      expect(chartDataLineUniqueUsersComputedProperty.labels).toEqual(comp.$data.dateDataList);
      expect(chartDataLineUniqueUsersComputedProperty.datasets[0].label).toEqual('Unique Users');
      expect(chartDataLineUniqueUsersComputedProperty.datasets[0].data).toEqual(comp.$data.uniqueUsersDataList);

      (comp as any).selectPeriod('Last 7 days'); // trigger last 7 days selection

      expect(comp.$data.dateDataList.length).toEqual(7);
      expect(comp.$data.uniqueUsersDataList.length).toEqual(7);
    });

    it('should calculate chartDataLineIntents', async () => {
      // last 30 days
      let chartDataLineIntentsComputedProperty = (comp as any).chartDataLineIntents;
      expect(chartDataLineIntentsComputedProperty.labels).toEqual(comp.$data.dateDataList);
      expect(chartDataLineIntentsComputedProperty.datasets[0].label).toEqual('intent1');
      expect(chartDataLineIntentsComputedProperty.datasets[0].data).toEqual(
        [5, 2, 3, 8, 11, 4, 0, 2],
      );

      comp.$data.period = 'Last 7 days'; // trigger last 7 days selection
      chartDataLineIntentsComputedProperty = (comp as any).chartDataLineIntents;
      expect(chartDataLineIntentsComputedProperty.datasets[0].data).toEqual(
        [2, 3, 8, 11, 4, 0, 2],
      );
    });

    it('should calculate chartDataBarFallback', async () => {
      // last 30 days
      const chartDataBarFallbackComputedProperty = (comp as any).chartDataBarFallback;
      expect(chartDataBarFallbackComputedProperty.labels).toEqual(comp.$data.dateDataList);
      expect(chartDataBarFallbackComputedProperty.datasets[0].label).toEqual('Fallback');
      expect(chartDataBarFallbackComputedProperty.datasets[0].data).toEqual(
        [3, 0, 3, 3, 3, 1, 3, 5],
      );

      (comp as any).selectPeriod('Last 7 days'); // trigger last 7 days selection

      expect(comp.$data.dateDataList.length).toEqual(7);
      expect(comp.$data.uniqueUsersDataList.length).toEqual(7);
    });

    it('should calculate chartDoghnutIntents', async () => {
      let chartDoghnutIntentComputedProperty;

      // last 30 days
      chartDoghnutIntentComputedProperty = (comp as any).chartDoghnutIntents;

      expect(chartDoghnutIntentComputedProperty.datasets[0].data).toEqual(
        [35, 8, 21, 1, 1],
      );

      // last day
      (comp as any).selectPeriodForDoghnut('Last day');
      chartDoghnutIntentComputedProperty = (comp as any).chartDoghnutIntents;
      expect(chartDoghnutIntentComputedProperty.labels).toEqual(comp.$data.intentDataList);
      expect(chartDoghnutIntentComputedProperty.datasets[0].data).toEqual(
        [2, 1, 5, 0, 1],
      );

      (comp as any).selectPeriodForDoghnut('Last 7 days'); // trigger last 7 days selection
      chartDoghnutIntentComputedProperty = (comp as any).chartDoghnutIntents;

      expect(chartDoghnutIntentComputedProperty.datasets[0].data).toEqual(
        [30, 7, 18, 1, 1],
      );
    });
  });
});
