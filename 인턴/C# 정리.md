C#

문자열을 정수형으로 바꿀 때 사용하는 방법

```c#
string srcIP = "192.168.1.50";
int src_idx = Int32.Parse(srcIP.Substring(10));
```

srcIP의 10번째 문자부터 정수형으로 만듦



```c#
public static List<IPAddress> arr_ip = new List<IPAddress>();
sort_ip = arr_ip.OrderBy(i => new Version(i.ToString())).ToList();
```

위의 IPAddress List 속성인 arr_ip를 ip 순서에 맞게 리스트로 만들어 sort_ip에  넣어준다. 사용할 시에 sort_ip를 미리 선언해 주어야 한다. 



```c#
srcIP.Substring(0, 10) + arr_idx[i - 1].ToString()
```

문자열과 변수를 합칠 때 이런 식으로 사용하면 된다.



```C#
int IP_range = dst_idx- src_idx + 1;
int split_cnt = 0;
double term_idx = 0;

term_idx = IP_range / split_cnt;

```

나눌 때 이런 식으로 해줘야 에러가 뜨지 않고 계산이 됬음



리스트에서 중복 값 제거 할 때

```1c#
sort_ip = arr_ip.Distinct()
```



UI에 있는 Name 객체를 cs 내부로 들고 와서 사용하고 싶을 때 

```c#
if (!this.Dispatcher.CheckAccess())
{
    this.Dispatcher.Invoke(new Action(delegate ()
    {
    	progressBar1.Value = count_th;
        if (count_th== split_cnt) 
        {
        	Progress_btn.Visibility = Visibility.Visible;
         }
     }));

}
```

위와 같은 형태로 사용하면 된다. progressbar의 name이 progressBar1인 것의 Value 값을 변경 해주고, Progress_btn을 visible하게 변경 해준다.