import { twelveHourFormJsonInfoType } from '@/types/Forms/MV2906';
import { VuexModule, Module, Mutation, Action } from 'vuex-module-decorators';

@Module({
  namespaced: true
})
class MV2906 extends VuexModule {

    public mv2906FormsJson: twelveHourFormJsonInfoType[] = [];
    public mv2906Info = {} as twelveHourFormJsonInfoType;  
    
      
    @Mutation
    public setMV2906FormsJson(mv2906FormsJson: twelveHourFormJsonInfoType[]): void {   
        this.mv2906FormsJson = mv2906FormsJson;
    }    
    @Action
    public UpdateMV2906FormsJson(newMV2906FormsJson: twelveHourFormJsonInfoType[]): void {
        this.context.commit('setMV2906FormsJson', newMV2906FormsJson);
    }
  
    @Mutation
    public setMV2906Info(mv2906Info: twelveHourFormJsonInfoType): void {   
        this.mv2906Info = mv2906Info;        
    }    
    @Action
    public UpdateMV2906Info(newMV2906Info: twelveHourFormJsonInfoType): void {
        this.context.commit('setMV2906Info', newMV2906Info);        
    } 

    
}

export default MV2906