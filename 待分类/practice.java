public class WordCountMapper extends Mapper <LongWritable, Text, Text, IntWritable>{
  Text k = new Text();
  IntWritable v = new IntWriteable(1);

  @Override
  public void map(LongWritable key, Text values, Context context) throws IOException, InterruptedException {
   
   String[] words = values.toString().split(" ");

   for(String word : words){
       k.set(word)
       context.write(k,v);
   }
  }
}

public class WordCountReducer extends Reducer <LongWritable, Text, Text, IntWritable> {

  int sum;
  IntWritable v = new IntWritable();

  @Override
  public void reducer(LongWritable key, Iterable<IntWritable> values, Context context) throws IOException, InterruptedException {
    sum = 0;
    for(int count : values) {
        sum += count;
    }
    v.set(sum);
    context.write(k,v);
  }
}